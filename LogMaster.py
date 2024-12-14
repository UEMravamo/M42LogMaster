import datetime as dt
import time
from log_processor import preprocess_date, process_log_file_binary, format_connections

if __name__ == "__main__":
    # Cronómetro de inicio
    start = time.time()

    # Configuración de fechas
    init_datetime_str = preprocess_date("Martes, 13 de agosto de 2019 01:00:00")
    end_datetime_str = preprocess_date("Martes, 13 de agosto de 2019 21:00:00")
    datetime_format = "%A, %d de %B de %Y %H:%M:%S"
    init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
    end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

    log_file = 'input-file-10000-2.txt'
    host = 'Aadvik'

    # Procesar conexiones
    try:
        connections = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(connections, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")

    # Cronómetro de fin
    end = time.time()
    print(f"Tiempo total de ejecución: {end - start:.10f} segundos ")
