# Librería para procesamiento y análisis de logs
from datetime import datetime
import itertools
from collections import defaultdict
import multiprocessing
import os
import networkx as nx
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, window, count, desc, split, length
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.file_manager import preprocess_date

### Version secuencial ###

### Version Grafo ###
# Función para leer el archivo de log y construir el grafo
def build_graph(log_file):
    # Inicializamos el grafo
    G = nx.DiGraph()

    # Leemos el log
    with open(log_file, 'r') as f:
        for line in f:
            # Procesar línea del log y generar partes del grafo
            parts = line.strip().split()
            timestamp = int(parts[0])
            host_from = parts[1]
            host_to = parts[2]

            # Convertir timestamp a formato datetime
            timestamp_datetime = datetime.utcfromtimestamp(timestamp / 1000)
            timestamp_str = timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Añadir nodos (hosts) al grafo
            if not G.has_node(host_from):
                G.add_node(host_from)
            if not G.has_node(host_to):
                G.add_node(host_to)

            # Añadir aristas (conexiones entre hosts) con atributo timestamp formateado
            G.add_edge(host_from, host_to, timestamp=timestamp_str)

    # Imprimir grafo
    print(
        f"\n  - Grafo generado exitosamente con {G.number_of_nodes()} nodos(hosts) y (aristas) {G.number_of_edges()} aristas.\n")

    print("  - Primeros Nodos (hosts) del grafo:")
    for node in itertools.islice(G.nodes, 10):
        print("\t", node)

    print("\n  - Primeras Aristas (Conexiones) del grafo:")
    for host_from, host_to, data in itertools.islice(G.edges(data=True), 10):
        timestamp = data.get('timestamp', 'No timestamp')
        print(f"\t{timestamp} - {host_from} --> {host_to}")

    return G
def find_connections_in_time_range(grafo, hostname, start_time, end_time):
    # Diccionario para almacenar las conexiones entrantes y salientes
    connections = {
        'entrantes': defaultdict(int),  # Conexiones entrantes
        'salientes': defaultdict(int)  # Conexiones salientes
    }

    # Evitamos errores al comparar fechas comprobando que start_time y end_time son objetos datetime
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # Iterar sobre las aristas del grafo
    for edge in grafo.edges(data=True):
        host_from, host_to, data = edge
        timestamp = data['timestamp']

        # Evitamos errores al comparar fechas pasando timestamp a datetime si es una cadena
        if isinstance(timestamp, str):
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        # Verificar si el timestamp está dentro del rango
        if start_time <= timestamp <= end_time:
            if host_from == hostname:
                # Si el host especificado es el origen, añadimos al diccionario de salientes
                connections['salientes'][host_to] += 1
            elif host_to == hostname:
                # Si el host especificado es el destino, añadimos al diccionario de entrantes
                connections['entrantes'][host_from] += 1

    return connections


#### Versión concurrente ####
def process_chunk_binary(chunk, init_, end_, target_host):
    """Procesa un fragmento binario decodificado como texto."""
    conns_in, conns_out = defaultdict(int), defaultdict(int)
    lines = chunk.splitlines()  # Divide en líneas

    for line in lines:
        try:
            # Dividir línea en partes
            parts = line.split()
            # Convertir timestamp a segundos
            timestamp = int(parts[0]) // 1000
            # Extraer hosts
            src_host, dst_host = parts[1], parts[2]
        except (ValueError, IndexError):
            # Si hay un error, pasar a la siguiente línea
            continue

        # Solo procesar si el timestamp está dentro del rango + 5 minutos
        if (init_ - 300) <= timestamp <= (end_ + 300):
            if src_host == target_host:
                conns_out[dst_host] += 1
            if dst_host == target_host:
                conns_in[src_host] += 1

    return conns_in, conns_out

def merge_results(results):
    """Combina los resultados parciales."""
    final_in, final_out = defaultdict(int), defaultdict(int)

    try:
        for conns_in, conns_out in results:
            for host, count in conns_in.items():
                final_in[host] += count
            for host, count in conns_out.items():
                final_out[host] += count
    except Exception as e:
        raise RuntimeError(f"Error al combinar resultados: {e}")

    return {'entrantes': final_in, 'salientes': final_out}

def process_log_file_binary(file_, init_, end_, target_host, num_workers=None):
    """
    Procesa el archivo en modo binario, dividiéndolo en bloques, y decodifica las líneas.
    """
    if num_workers is None:
        num_workers = os.cpu_count()

    init_ = int(init_.timestamp())
    end_ = int(end_.timestamp())
    chunk_size = 1024 * 1024  # Leer en bloques de 1 MB

    results = []
    pool = multiprocessing.Pool(num_workers)
    # Leer archivo en bloques
    try:
        with open(file_, 'rb') as f:
            # Este trozo se explica en Explanation.md
            leftover = b""  # Esto hace que sea una cadena de bytes
            while chunk := f.read(chunk_size):
                chunk = leftover + chunk
                try:
                    last_newline = chunk.rindex(b'\n')
                    leftover = chunk[last_newline + 1:]
                    chunk = chunk[:last_newline]
                except ValueError:
                    leftover = chunk
                    continue
                try:
                    decoded_chunk = chunk.decode('utf-8')  # Decodificar como texto
                except UnicodeDecodeError as e:
                    print(f"Error al decodificar fragmento: {e}")
                    continue

                # Procesar el fragmento en paralelo
                results.append(pool.apply_async(process_chunk_binary, (decoded_chunk, init_, end_, target_host)))
    except (OSError, IOError) as e:
        raise FileNotFoundError(f"Error al leer el archivo {file_} : {e}")
    finally:
        pool.close()
        pool.join()

    # Combinar resultados parciales
    try:
        processed_results = [res.get() for res in results]
        return merge_results(processed_results)
    except Exception as e:
        raise RuntimeError(f"Error al combinar resultados: {e}")
    

##Version Distribuida con Spark##

#Asegurar que el directorio lib está en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))

def process_log_spark(log_file, hostname, start_datetime_str, end_datetime_str, datetime_format="%A, %d de %B de %Y %H:%M:%S"):
    spark = None
    try:
        print("Configurando Spark...")
        
        # Configuración más ligera de Spark
        spark = (SparkSession.builder
            .appName("LogProcessorSpark")
            .config("spark.driver.memory", "1g")
            .config("spark.executor.memory", "1g")
            .config("spark.sql.session.timeZone", "UTC")
            .config("spark.driver.maxResultSize", "1g")
            .config("spark.driver.bindAddress", "127.0.0.1")  # Forzar localhost
            .config("spark.driver.host", "127.0.0.1")        # Forzar localhost
            .master("local[2]")  # Usar solo 2 cores en lugar de todos
            .getOrCreate())

        # Reducir el nivel de log de Spark
        spark.sparkContext.setLogLevel("ERROR")
        
        print("SparkSession creada exitosamente")
        
        # Convertir fechas
        print("Procesando fechas...")
        start_datetime = datetime.strptime(preprocess_date(start_datetime_str), datetime_format)
        end_datetime = datetime.strptime(preprocess_date(end_datetime_str), datetime_format)
        
        print(f"Leyendo archivo: {log_file}")
        # Leer el archivo de log como un dataframe con schema explícito
        df = spark.read.text(log_file)
        print(f"Registros totales leídos: {df.count()}")

        # Procesar y transformar los datos
        print("Transformando datos...")
        df = df.select(
            (col("value").substr(1, 10).cast("long") * 1000).alias("timestamp"),
            split(col("value"), " ")[1].alias("host_from"),
            split(col("value"), " ")[2].alias("host_to")
        ).cache()  # Cachear el DataFrame para mejor rendimiento

        # Convertir timestamp a datetime
        df = df.withColumn("datetime", to_timestamp(col("timestamp") / 1000))
        
        print("Aplicando filtros temporales...")
        df_filtered = df.filter(
            (col("datetime") >= start_datetime) & 
            (col("datetime") <= end_datetime)
        ).cache()

        print(f"Buscando conexiones para el host: {hostname}")
        # Filtrar y contar conexiones
        connections_in = df_filtered.filter(col("host_to") == hostname)
        connections_out = df_filtered.filter(col("host_from") == hostname)

        # Agregar y ordenar resultados
        incoming_connections = connections_in.groupBy("host_from") \
            .agg(count("*").alias("count")) \
            .orderBy(desc("count"))

        outgoing_connections = connections_out.groupBy("host_to") \
            .agg(count("*").alias("count")) \
            .orderBy(desc("count"))

        # Forzar la evaluación de los DataFrames
        incoming_count = incoming_connections.count()
        outgoing_count = outgoing_connections.count()
        
        print(f"Conexiones encontradas - Entrantes: {incoming_count}, Salientes: {outgoing_count}")
        
        return incoming_connections, outgoing_connections

    except Exception as e:
        print(f"Error en el procesamiento Spark: {str(e)}")
        raise e

    finally:
        if spark:
            print("Cerrando sesión Spark...")
            spark.stop()
            print("Sesión Spark cerrada")
