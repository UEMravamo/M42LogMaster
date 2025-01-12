import sys
import os
import psutil
import time
import datetime as dt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.logs_processor import build_graph, find_connections_in_time_range
from lib.file_manager import preprocess_date, format_connections
from lib.logs_processor import process_log_file_binary

# Función para monitorear recursos
def monitor_resources(stage="Inicio"):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    print(f"[{stage}] Uso de CPU: {cpu_percent}% | Uso de memoria: {memory_info.percent}%")
    return cpu_percent, memory_info.percent

# Función de pruebas
def run_tests():
    print("\nEjecutando pruebas...")

    # Prueba 1: Verificar que el archivo existe
    test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input-file-10000.txt'))
    if not os.path.exists(test_file):
        print(f"Prueba 1: Fallo - El archivo '{test_file}' no existe.")
    else:
        print("Prueba 1: Éxito - El archivo existe.")

    # Prueba 2: Validar fechas correctas
    try:
        init_datetime_str = "Martes, 13 de agosto de 2019 01:00:00"
        end_datetime_str = "Martes, 13 de agosto de 2019 21:00:00"
        datetime_format = "%A, %d de %B de %Y %H:%M:%S"

        init_datetime_str = preprocess_date(init_datetime_str)
        end_datetime_str = preprocess_date(end_datetime_str)

        init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
        end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

        assert init_datetime < end_datetime, "La fecha inicial no es anterior a la fecha final."
        print("Prueba 2: Éxito - Fechas válidas.")
    except Exception as e:
        print(f"Prueba 2: Fallo - {e}")

    # Prueba 3: Procesar un archivo inexistente
    try:
        process_log_file_binary("archivo_inexistente.txt", init_datetime, end_datetime, "HostTest")
        print("Prueba 3: Fallo - No se detectó el archivo inexistente.")
    except FileNotFoundError:
        print("Prueba 3: Éxito - Se detectó el archivo inexistente correctamente.")
    except Exception as e:
        print(f"Prueba 3: Fallo - Error inesperado: {e}")

    # Prueba 4: Host vacío
    try:
        invalid_host = ""
        if not isinstance(invalid_host, str) or not invalid_host.strip():
            raise ValueError("El host es inválido.")
        print("Prueba 4: Fallo - Host vacío no fue detectado.")
    except ValueError:
        print("Prueba 4: Éxito - Host vacío detectado correctamente.")
    except Exception as e:
        print(f"Prueba 4: Fallo - Error inesperado: {e}")

    print("\nPruebas completadas.")

def main():
    # Monitorear antes de iniciar el proceso
    monitor_resources("Antes de iniciar")

    # Cronómetro de inicio
    start = time.time()

    # Configuración de variables
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'input-file-10000.txt'))
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

    # Monitorear después de la configuración
    monitor_resources("Después de configuración")

    # Procesar conexiones
    try:
        connections = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(connections, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")
    except Exception as e:
        print(f"Error inesperado durante el procesamiento de conexiones: {e}")

    # Monitorear después de procesar conexiones
    monitor_resources("Después de procesamiento")

    # Cronómetro de fin
    end = time.time()

    # Monitorear al final
    monitor_resources("Al final")

    print(f"Tiempo total de ejecución: {end - start:.10f} segundos")

    # Ejecutar pruebas
    run_tests()

if __name__ == "__main__":
    main()
