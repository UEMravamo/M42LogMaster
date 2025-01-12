import psutil
import time
import os
from functools import wraps

def measure_resources(func):
    """
    Decorador para medir el uso de recursos (CPU, memoria) y el tiempo de ejecución de una función.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtener el proceso actual
        process = psutil.Process(os.getpid())

        # Medir el uso de memoria antes de la ejecución
        start_memory = process.memory_info().rss / (1024 * 1024)  # Convertir a MB

        # Medir la carga de CPU antes de la ejecución
        start_cpu = process.cpu_percent(interval=None)

        # Medir el tiempo de inicio
        start_time = time.time()

        # Ejecutar la función
        result = func(*args, **kwargs)

        # Medir el tiempo de fin
        end_time = time.time()

        # Medir la carga de CPU después de la ejecución
        end_cpu = process.cpu_percent(interval=None)

        # Medir el uso de memoria después de la ejecución
        end_memory = process.memory_info().rss / (1024 * 1024)  # Convertir a MB

        # Imprimir los resultados
        print(f"\nFunción: {func.__name__}")
        print(f"Uso de memoria promedio: {end_memory - start_memory:.4f} MB")
        print(f"Tiempo de ejecución promedio: {end_time - start_time:.4f} s")
        print(f"Carga de CPU de la función promedio: {end_cpu - start_cpu:.4f}%")

        return result
    return wrapper