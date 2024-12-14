# Script para listar conexiones de un host en un periodo de tiempo

import datetime as dt
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.file_manager import preprocess_date, format_connections
from lib.log_procesor import process_log_file_binary

if __name__ == "__main__":
    # Cronómetro de inicio
    start = time.time()

    # Configuración de variables
    log_file = '../data/input-file-10000-2.txt'
    host = 'Savhannah'
    init_datetime_str = "Martes, 13 de agosto de 2019 01:00:00"
    end_datetime_str = "Martes, 13 de agosto de 2019 21:00:00"
    datetime_format = "%A, %d de %B de %Y %H:%M:%S"

    # Validar el archivo
    if not os.path.exists(log_file):
        print(f"Error: El archivo '{log_file}' no existe.")
        sys.exit(1)

    # Validar el host
    if not isinstance(host, str) or not host.strip():
        print("Error: El valor del host no es válido. Debe ser una cadena no vacía.")
        sys.exit(1)

    # Preprocesar y validar fechas
    try:
        init_datetime_str = preprocess_date(init_datetime_str)
        end_datetime_str = preprocess_date(end_datetime_str)
        init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
        end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

        if init_datetime >= end_datetime:
            raise ValueError("La fecha inicial debe ser anterior a la fecha final.")
    except ValueError as e:
        print(f"Error en la configuración de fechas: {e}")
        sys.exit(1)

    # Procesar conexiones
    try:
        connections = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(connections, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")
    except Exception as e:
        print(f"Error inesperado durante el procesamiento de conexiones: {e}")

    # Cronómetro de fin
    end = time.time()
    print(f"Tiempo total de ejecución: {end - start:.10f} segundos ")
