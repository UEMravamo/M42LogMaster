from collections import defaultdict
import  datetime as dt
import time

#iniciar crono
start = time.time()

# Diccionario para traducir días y meses de español a inglés
spanish_to_english = {
    "Lunes": "Monday", "Martes": "Tuesday", "Miércoles": "Wednesday",
    "Jueves": "Thursday", "Viernes": "Friday", "Sábado": "Saturday", "Domingo": "Sunday",
    "enero": "January", "febrero": "February", "marzo": "March",
    "abril": "April", "mayo": "May", "junio": "June",
    "julio": "July", "agosto": "August", "septiembre": "September",
    "octubre": "October", "noviembre": "November", "diciembre": "December",
}

def preprocess_date(date_str):
    """Reemplaza los nombres en español de días y meses por su equivalente en inglés (No me deja instalar la lib 'locale')."""
    for spanish, english in spanish_to_english.items():
        date_str = date_str.replace(spanish, english)
    return date_str

def parse_log_file(file_path):
    """
    Generador que lee el archivo de log línea por línea y analiza cada una.
    """
    with open(file_path, 'r') as file:
        for line in file:
            parsed_line = parse_log_line(line)
            yield parsed_line, line

def parse_log_line(line):
    """analiza una línea del archivo y devuelve None si no es válida."""
    try:
        parts = line.strip().split()
        if len(parts) != 3:
            return None
        timestamp = int(parts[0])
        src_host = parts[1]
        dst_host = parts[2]
        return timestamp, src_host, dst_host
    except (ValueError, IndexError):
        return None

def read_log_file(log_file, init_datetime,end_datetime,target_host,time_tolerance=300):
    """
        Lee un archivo de log desde un generador para intentar consumir menos memoria
    """
    init_time = int(init_datetime.timestamp()) - time_tolerance
    end_time = int(end_datetime.timestamp()) + time_tolerance

#rango de fechas
init_datetime_str = "Martes, 13 de agosto de 2019 01:00:00"
end_datetime_str = "Martes, 13 de agosto de 2019 21:00:00"

# Formato esperado para las fechas
datetime_format = "%A, %d de %B de %Y %H:%M:%S"

# Preprocesar las fechas para convertirlas al formato en inglés
init_datetime_str = preprocess_date(init_datetime_str)
end_datetime_str = preprocess_date(end_datetime_str)

# Convertir las cadenas a objetos datetime
init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

print("Fecha de inicio: ", init_datetime)
print("Fecha de fin: ", end_datetime)

#cargar archivo
log_file = 'test.txt'
#Host a analizar
host = 'Savhannah'

print("Archivo a analizar: ", log_file)
print("Host a analizar: ", host)