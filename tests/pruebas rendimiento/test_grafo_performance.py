import timeit
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.log_procesor import build_graph

def test_performance():
    # Archivo de logs
    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input-file-10000.txt'))

    # Preparación de lo necesario para la función build_graph (import + archivo de logs)
    setup_build_graph = f"""
from lib.log_procesor import build_graph
log_file = r"{log_file.replace(os.sep, '/')}"
"""
    
    # Código a repetir X veces para build_graph
    stmt_build_graph = "build_graph(log_file)"

    # Ejecutamos el test 30 veces para build_graph
    build_graph_time = timeit.timeit(stmt=stmt_build_graph, setup=setup_build_graph, number=30)
    print(f"Tiempo promedio para build_graph: {build_graph_time / 30:.4f} segundos")

if __name__ == "__main__":
    test_performance()
