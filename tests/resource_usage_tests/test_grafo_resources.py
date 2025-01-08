import os
import sys
import time
from datetime import datetime
import psutil
from functools import wraps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.log_procesor import build_graph, find_connections_in_time_range

def measure_memory_and_cpu(func):

    # Definimos la envoltura de la función (lo que hará antes y después de ejecutar la función)
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        
        # Variables para acumular los sumatorios de medidas
        memory_usage_total = 0
        cpu_usage_function_total = 0
        execution_time_total = 0
        cpu_global_total_start = 0
        cpu_global_total_end = 0

        # Repeticiones de las mediciones para luego hacer un promedio
        repetitions = 30  

        for _ in range(repetitions):
            # Medimos la memoria usada ANTES de ejecutar la función
            start_memory = process.memory_info().rss / (1024 * 1024)  # Memoria en MB

            # Medimos la carga de CPU global ANTES de ejecutar la función
            cpu_global_total_start = psutil.cpu_percent(interval=2)

            # Medimos la carga de CPU del proceso ANTES de ejecutar la función
            start_cpu_function = process.cpu_percent(interval=2)

            # Iniciamos el cronómetro para medir el tiempo de ejecución de la función
            start_time = time.time()

            # Ejecutamos la función ##########################################
            result = func(*args, **kwargs)
            #################################################################

            # Medimos la memoria usada JUSTO DESPUÉS de terminar de ejecutar la función
            end_memory = process.memory_info().rss / (1024 * 1024)

            # Medimos la carga de CPU global JUSTO DESPUÉS de terminar de ejecutar la función
            cpu_global_total_end = psutil.cpu_percent(interval=2)

            # Medimos la carga de CPU del proceso JUSTO DESPUÉS de terminar de ejecutar la función
            end_cpu_function = process.cpu_percent(interval=2)

            # Detenemos el cronómetro para medir el tiempo de ejecución
            end_time = time.time()

            # Calculamos la diferencia de memoria antes y JUSTO DESPUÉS de ejecutar la función
            memory_usage = end_memory - start_memory

            # Calculamos el tiempo total de ejecución
            execution_time = end_time - start_time

            # Calculamos la diferencia de carga de CPU antes y JUSTO DESPUÉS de ejecutar la función
            cpu_usage_function = end_cpu_function - start_cpu_function

            # Calculamos la media de la carga de CPU global entre el valor antes y JUSTO DESPUÉS de ejecutar la función
            cpu_global = (cpu_global_total_start + cpu_global_total_end) / 2

            # Calculamos la diferencia de carga de CPU GLOBAL antes y JUSTO DESPUÉS de ejecutar la función# Incremento de la carga de CPU global
            increment_cpu_global = cpu_global_total_end - cpu_global_total_start

            # Sumamos los resultados a las variables sumatorias
            memory_usage_total += memory_usage
            execution_time_total += execution_time
            cpu_usage_function_total += cpu_usage_function

        # Calculamos los promedios
        memory_usage_avg = memory_usage_total / repetitions
        execution_time_avg = execution_time_total / repetitions
        cpu_usage_function_avg = cpu_usage_function_total / repetitions

        # Imprimimos los resultados
        print("\n----------------------------------------------------------------")
        print(f"Función: {func.__name__}")
        print(f"Uso de memoria promedio: {memory_usage_avg:.4f} MB")
        print(f"Tiempo de ejecución promedio: {execution_time_avg:.4f} s")
        print(f"Carga de CPU de la función promedio: {cpu_usage_function_avg:.4f}%")
        print(f"Carga de CPU global: {cpu_global:.4f}%")
        print(f"Incremento de carga de CPU global: {increment_cpu_global:.4f}%")
        print("----------------------------------------------------------------\n")

        return result
    return wrapper

@measure_memory_and_cpu
def test_build_graph():
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input-file-10000.txt'))
    return build_graph(log_file)

@measure_memory_and_cpu
def test_find_connections_in_time_range(grafo):
    start_time = datetime.fromtimestamp(1672531200)
    end_time = datetime.fromtimestamp(1672531300)
    return find_connections_in_time_range(grafo, 'hostname_example', start_time, end_time)

if __name__ == "__main__":
    grafo = test_build_graph()
    test_find_connections_in_time_range(grafo)