import datetime as dt
import time
from collections import defaultdict

# Cronómetro de inicio
start = time.time()

def preprocess_date(date_str):
    """Convierte nombres de días y meses en español a inglés directamente, eliminamos recorrer varias veces el diccionario"""
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

def parse_log_line(line):
    """Parsea la linea y extrae cada parte"""
    try:
        parts = line.strip().split()
        timestamp = int(parts[0]) // 1000
        return timestamp, parts[1], parts[2]
    except (ValueError, IndexError):
        return None

def read_log_file(file_, init_, end_, target_host, time_tolerance=300):
    """
    Procesar las el archivo y sacar las conxiones en un rango determinado
    """
    init_ = int(init_.timestamp()) - time_tolerance
    end_ = int(end_.timestamp()) + time_tolerance

    conns = {'entrantes': defaultdict(int), 'salientes': defaultdict(int)}
    with open(file_, 'r') as file:
        for line in file:
            parsed_line = parse_log_line(line)
            if parsed_line is None:
                continue

            timestamp, src_host, dst_host = parsed_line
            if not (init_ <= timestamp <= end_):
                continue

            if src_host == target_host:
                conns['salientes'][dst_host] += 1
            if dst_host == target_host:
                conns['entrantes'][src_host] += 1

    return conns

def format_connections(conns, server_name):
    """
    Formatear el output para ver el numero de conexiones por host
    """
    formatted = [f"Conexiones del servidor: {server_name}"]
    for direction, hosts in conns.items():
        formatted.append(f"Conexiones {direction}:")
        for host_, count in hosts.items():
            formatted.append(f"  - {host_}: {count} conexiones")
    return '\n'.join(formatted)

# Proceso principal
init_datetime_str = preprocess_date("Martes, 13 de agosto de 2019 01:00:00")
end_datetime_str = preprocess_date("Martes, 13 de agosto de 2019 21:00:00")

datetime_format = "%A, %d de %B de %Y %H:%M:%S"
init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

log_file = 'input-file-10000.txt'
host = 'Savhannah'

try:
    connections = read_log_file(log_file, init_datetime, end_datetime, host)
    print(format_connections(connections, host))
except FileNotFoundError:
    print(f"Error: El archivo '{log_file}' no existe.")

end = time.time()
print(f"Tiempo total de ejecución: {end - start:.10f} segundos ")
