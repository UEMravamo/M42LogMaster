import os
import sys
from datetime import datetime
import psutil
from functools import wraps

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.log_procesor import build_graph, find_connections_in_time_range

def measure_memory(func):

    # Definimos la envoltura de la función (lo que ará antes y después de ejecutar la función)
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()

        # Medimos la memoria usada antes de llamar a la función
        start_memory = process.memory_info().rss / (1024 * 1024)

        # Ejecutar la función
        result = func(*args, **kwargs)

        # Medimos la memoria usada después de llamar a la función JUSTO DESPUÉS de que la función termine
        end_memory = process.memory_info().rss / (1024 * 1024)

        # Calcular diferencia de memoeria nates y después
        memory_usage = end_memory - start_memory
        
        # Imprimimos resultados
        print(f"Función: {func.__name__}")
        print(f"Uso de memoria: {memory_usage:.4f} MB")

        return result
    return wrapper

# Añadimos el decorador de @measure_memory a test_build_graph() para poder medir la memoria utilizada antes y después de ejecutar la función
@measure_memory
def test_build_graph():
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input-file-10000.txt'))
    return build_graph(log_file)
 
# Añadimos el decorador de @measure_memory a test_find_connections_in_time_range() para poder medir la memoria utilizada antes y después de ejecutar la función
@measure_memory
def test_find_connections_in_time_range(grafo):
    # Definimos start_time y end_time como objetos datetime para pasarle a la función como rango de búsqueda
    start_time = datetime.fromtimestamp(1672531200)
    end_time = datetime.fromtimestamp(1672531300)
    return find_connections_in_time_range(grafo, 'hostname_example', start_time, end_time)

if __name__ == "__main__":
    # LLamamos a test_build_graph con el decorador para medir la memoria utilizada antes y después de ejecutar la función
    grafo = test_build_graph()

   # LLamamos a test_find_connections con el decorador para medir la memoria utilizada antes y después de ejecutar la función
    test_find_connections_in_time_range(grafo)