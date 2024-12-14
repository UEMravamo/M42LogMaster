# Librería para procesamiento y análisis de logs

from collections import defaultdict
import multiprocessing
import os

# Versión tradicional

# Versión concurrente
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

        # Solo procesar si el timestamp está dentro del rango
        if init_ <= timestamp <= end_:
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
            leftover = b"" # Esto hace que sea una cadena de bytes
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

# Versión distribuida con Spark

# versión distribuida con Hadoop

# Versión distribuida con Dask

# Versión distribuida con Ray