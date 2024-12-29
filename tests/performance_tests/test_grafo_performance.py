import timeit
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.log_procesor import build_graph, find_connections_in_time_range

def test_performance():
    # Archivo de logs
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input-file-10000.txt'))

    # Prerequisitos y precondiciones para ejecutar la función build_graph (import + archivo de logs)
    setup_build_graph = f"""
# Importar función de la librería
from lib.log_procesor import build_graph
# Ruta al archivo de logs
log_file = r"{log_file.replace(os.sep, '/')}"
"""

    # Prerequisitos y precondiciones para ejecutar la función find_connections_in_time_range (import + archivo de logs)
    setup_find_connections = f"""
# Importar función de la librería
from lib.log_procesor import find_connections_in_time_range, build_graph
from datetime import datetime  # Añadido aquí la importación de datetime
# Ruta al archivo de logs
log_file = r"{log_file.replace(os.sep, '/')}"

# Definimos start_time y end_time como objetos datetime para pasarle a la función como rango de búsqueda
start_time = datetime.fromtimestamp(1672531200)
end_time = datetime.fromtimestamp(1672531300)

# Construir un grafo
grafo = build_graph(log_file)
"""

    # Código a repetir X veces para build_graph
    stmt_build_graph = "build_graph(log_file)"

    # Código a repetir X veces para find_connections_in_time_range (con start_time y end_time)
    stmt_find_connections = "find_connections_in_time_range(grafo, 'hostname_example', start_time, end_time)"

    # Ejecutamos el test X veces para build_graph
    build_graph_time = timeit.timeit(stmt=stmt_build_graph, setup=setup_build_graph, number=50)
    
    # Ejecutamos el test X veces para find_connections_in_time_range
    find_connections_time = timeit.timeit(stmt=stmt_find_connections, setup=setup_find_connections, number=50)

    print("----------------------------------------------------------------------------")
    print(f"Tiempo promedio para build_graph: {build_graph_time / 50:.4f} segundos")
    print(f"Tiempo promedio para find_connections_in_time_range: {find_connections_time / 50:.4f} segundos")
    print("----------------------------------------------------------------------------")
    
if __name__ == "__main__":
    test_performance()
