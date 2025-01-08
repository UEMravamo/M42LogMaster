import unittest
import networkx as nx
import os
import sys

# Configura el path para que Python pueda encontrar el directorio 'lib'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lib.log_procesor import build_graph, find_connections_in_time_range

class TestGraphFunctions(unittest.TestCase):

    # Creamos un grafo de ejemplo
    def setUp(self):
        self.grafo = nx.DiGraph()
        self.grafo.add_edge("HostA", "HostB", timestamp="2025-01-01 12:00:00")
        self.grafo.add_edge("HostA", "HostC", timestamp="2025-01-01 12:10:00")
        self.grafo.add_edge("HostB", "HostA", timestamp="2025-01-01 12:20:00")
        self.grafo.add_edge("HostC", "HostB", timestamp="2025-01-01 12:30:00")

# Test para comprobar que construye un grafo correctamente desde un archivo
    def test_build_graph(self):
        try:
            log_file = "test_log.txt"
            with open(log_file, "w") as f:
                f.write("1672531200000 HostA HostB\n")
                f.write("1672531300000 HostA HostC\n")
            graph = build_graph(log_file)
            self.assertEqual(graph.number_of_nodes(), 3)
            self.assertEqual(graph.number_of_edges(), 2)
            print("Test 1: Comprobar construcción de grafo: OK")
        except Exception as e:
            print(f"Test 1: Comprobar construcción de grafo: FAILED")
            print(f"Error: {e}")
        finally:
            # Eliminar el archivo después del test
            if os.path.exists(log_file):
                os.remove(log_file)

    # Test  para analizar si detecta correctamente las conexiones entrantes y salientes dentro del rango de tiempo especificado
    def test_find_connections_in_time_range(self):
        try:
            start_time = "2025-01-01 12:00:00"
            end_time = "2025-01-01 12:25:00"
            hostname = "HostA"
            result = find_connections_in_time_range(self.grafo, hostname, start_time, end_time)
            self.assertEqual(result['salientes'], {"HostB": 1, "HostC": 1})
            self.assertEqual(result['entrantes'], {"HostB": 1})
            print("Test 2: Comprobar conexiones en rango de tiempo: OK")
        except Exception as e:
            print(f"Test 2: Comprobar conexiones en rango de tiempo: FAILED")
            print(f"Error: {e}")

    # Test para analizar como gestiona grafos vacíos
    def test_empty_graph(self):
        try:
            empty_graph = nx.DiGraph()
            result = find_connections_in_time_range(empty_graph, "HostA", "2025-01-01 12:00:00", "2025-01-01 12:25:00")
            self.assertEqual(result['salientes'], {})
            self.assertEqual(result['entrantes'], {})
            print("Test 3: Comprobar grafos vacíos: OK")
        except Exception as e:
            print(f"Test 3: Comprobar grafos vacíos: FAILED")
            print(f"Error: {e}")

    # Test para analizar como gestiona timestamps erróneos
    def test_invalid_time_format(self):
        try:
            with self.assertRaises(ValueError):
                find_connections_in_time_range(self.grafo, "HostA", "invalid", "2025-01-01 12:25:00")
            print("Test 4: Comprobar manejo de formato de tiempo erróneo: OK")
        except Exception as e:
            print(f"Test 4: Comprobar manejo de formato de tiempo erróneo: FAILED")
            print(f"Error: {e}")

if __name__ == "__main__":
    unittest.main(verbosity=0) 