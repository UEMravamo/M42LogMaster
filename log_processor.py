from collections import defaultdict
import multiprocessing
import os

def preprocess_date(date_str):
    """Convierte nombres de días y meses en español a inglés directamente(no me funciona la librería locale)."""
    return (date_str
            .replace("Lunes", "Monday").replace("Martes", "Tuesday")
            .replace("Miércoles", "Wednesday").replace("Jueves", "Thursday")
            .replace("Viernes", "Friday").replace("Sábado", "Saturday")
            .replace("Domingo", "Sunday")
            .replace("enero", "January").replace("febrero", "February")
            .replace("marzo", "March").replace("abril", "April")
            .replace("mayo", "May").replace("junio", "June")
            .replace("julio", "July").replace("agosto", "August")
            .replace("septiembre", "September").replace("octubre", "October")
            .replace("noviembre", "November").replace("diciembre", "December"))

def process_trozo(trozo, init_, end_, target_host):
    """Procesa un trozo del archivo de log"""
    conns_entrantes, conns_salientes = defaultdict(int), defaultdict(int)

    for line in trozo:
        parts = line.split()
        try:
            # Convertir el timestamp a segundos
            timestamp = int(parts[0]) // 1000
            # Obtener los hosts
            src_host, dst_host = parts[1], parts[2]
        except (ValueError, IndexError):
            continue

        if not (init_ <= timestamp <= end_):
            continue

        if src_host == target_host:
            conns_salientes[dst_host] += 1
        if dst_host == target_host:
            conns_entrantes[src_host] += 1

    return conns_entrantes, conns_salientes

def combinar_results(results):
    """Combina los resultados"""
    entrantes, salientes = defaultdict(int), defaultdict(int)
    for conns_entrantes, conns_salientes in results:
        for host, count in conns_entrantes.items():
            entrantes[host] += count
        for host, count in conns_salientes.items():
            salientes[host] += count
    return {'entrantes': entrantes, 'salientes': salientes}

def process_log_file_paralelo(file_, init_, end_, target_host, procesos=None):
    """
    Procesa el archivo en paralelo dividiéndolo en bloques.
    """
    if procesos is None:
        procesos = os.cpu_count()

    init_ = int(init_.timestamp())
    end_ = int(end_.timestamp())
    trozo_size = 1024 * 1024  # Leer en bloques de 1 MB

    results = []
    # Leer el archivo en bloques
    with open(file_, 'r') as f:
        # Crear una pool de procesos
        pool = multiprocessing.Pool(procesos)
        # Leer el archivo en bloques de 1 MB mientras haya contenido
        while trozo := f.readlines(trozo_size):
            # Procesar el trozo en un proceso
            results.append(pool.apply_async(process_trozo, (trozo, init_, end_, target_host)))
        # Cerrar la pool para que no se puedan agregar más procesos
        pool.close()
        # Esperar a que todos los procesos terminen
        pool.join()

    # Combinar resultados parciales
    res_procesados = [res.get() for res in results]
    return combinar_results(res_procesados)

def format_connections(conns, server_name):
    """Formatea el output para ver el número de conexiones por host."""
    formatted = [f"Conexiones del servidor: {server_name}"]
    for direction, hosts in conns.items():
        formatted.append(f"Conexiones {direction}:")
        for host_, count in hosts.items():
            formatted.append(f"  - {host_}: {count} conexiones ")
    return '\n'.join(formatted)
