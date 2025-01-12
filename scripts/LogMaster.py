# Script para listar conexiones de un host y generar un grafo a partir del log

import datetime as dt
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.file_manager import preprocess_date, format_connections
from lib.logs_processor import process_log_file_binary, build_graph, find_connections_in_time_range
from lib.logs_processor import process_log_spark

if __name__ == "__main__":
    
    # Configuración de variables
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/input-file-10000.txt'))
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
        
    print("\n....................................................................................................")
    print("Buscando conexiones al hot ",host,"entre ",init_datetime," y ", end_datetime)
    print("....................................................................................................\n")

    #### V1- PROCESADO SECUENCIAL ####
    print("\n-------------------------------------------------------------------------------------------")
    print("MÉTODO 1: PROCESADO SECUENCIAL")
    print("-------------------------------------------------------------------------------------------\n")


    #### V2-PROCESADO CON GRAFO ####
    print("\n-------------------------------------------------------------------------------------------")
    print("MÉTODO 2: GRAFO")
    print("-------------------------------------------------------------------------------------------\n")

    # Creamos el grafo
    try:
        graph = build_graph(log_file)
    except Exception as e:
        print(f"Error al generar el grafo: {e}")
        sys.exit(1)

    # Buscamos las conexiones
    try:
        connected_hosts = find_connections_in_time_range(graph, host, init_datetime, end_datetime)
        
        if connected_hosts:
            print(format_connections(connected_hosts, host))
           
        else:
            print(f"\nNo se encontraron hosts conectados ")

    except Exception as e:
        print(f"Error al obtener las conexiones: {e}")


    #### V3 -PROCESADO CONCURRENTE ####
    print("\n-------------------------------------------------------------------------------------------")
    print("MÉTODO 3: PROCESAMIENTO CONCURRENTE")
    print("-------------------------------------------------------------------------------------------\n")
    
    try:
        connections = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(connections, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")
    except Exception as e:
        print(f"Error inesperado durante el procesamiento de conexiones: {e}")
    
    
    #### PROCESADO DISTRIBUIDO ####
    print("\n-------------------------------------------------------------------------------------------")
    print("MÉTODO 4: PROCESAMIENTO DISTRIBUIDO CON SPARK")
    print("-------------------------------------------------------------------------------------------\n")

    # Cronómetro de inicio
    start = time.time()

    # Procesamiento con Spark
    try:
        incoming_connections, outgoing_connections = process_log_spark(log_file, host, init_datetime_str, end_datetime_str, datetime_format)
        
        if incoming_connections and outgoing_connections:
            print("\nConexiones entrantes:")
            incoming_connections.show(truncate=False)
            print("\nConexiones salientes:")
            outgoing_connections.show(truncate=False)
        
    except Exception as e:
        print(f"Error en el procesamiento con Spark: {e}")
    finally:
        # Cronómetro de fin
        end = time.time()
        print("\n-------------------------------------------------------------------------------------------")
        print(f"Método 4 - Procesamiento distribuido con Spark: Tiempo total de ejecución: {end - start:.10f} segundos.\n")
        print("-------------------------------------------------------------------------------------------\n")











