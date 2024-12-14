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
    for conns_in, conns_out in results:
        for host, count in conns_in.items():
            final_in[host] += count
        for host, count in conns_out.items():
            final_out[host] += count
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

            decoded_chunk = chunk.decode('utf-8')  # Decodificar como texto
            # Procesar el fragmento en paralelo
            results.append(pool.apply_async(process_chunk_binary, (decoded_chunk, init_, end_, target_host)))

    pool.close()
    pool.join()

    # Combinar resultados parciales
    processed_results = [res.get() for res in results]
    return merge_results(processed_results)

def format_connections(conns, server_name):
    """Formatea el output para ver el número de conexiones por host."""
    formatted = [f"Conexiones del servidor: {server_name}"]
    for direction, hosts in conns.items():
        formatted.append(f"Conexiones {direction}:")
        for host_, count in hosts.items():
            formatted.append(f"  - {host_}: {count} conexiones ")
    return '\n'.join(formatted)
