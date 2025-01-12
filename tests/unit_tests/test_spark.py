# tests/test_unit.py
import pytest
from lib.file_manager import preprocess_date, format_connections
from lib.logs_processor import build_graph, find_connections_in_time_range

def test_preprocess_date():
    assert preprocess_date("Martes, 13 de agosto de 2019 01:00:00") == "Tuesday, 13 de August de 2019 01:00:00"
    assert preprocess_date("Viernes, 1 de enero de 2021 10:00:00") == "Friday, 1 de January de 2021 10:00:00"

def test_format_connections():
    connections = {
        'entrantes': {'HostA': 5, 'HostB': 2},
        'salientes': {'HostC': 1, 'HostD': 8}
    }
    expected_output = (
        "\n  - Conexiones del host: TestHost\n"
        "\n \t Conexiones Entrantes:\n"
        "\t  - HostA: 5 conexiones\n"
        "\t  - HostB: 2 conexiones\n"
        "\n \t Conexiones Salientes:\n"
        "\t  - HostC: 1 conexión\n"
        "\t  - HostD: 8 conexiones"
    )
    assert format_connections(connections, "TestHost") == expected_output

def test_build_graph(sample_log_file):
    graph = build_graph(sample_log_file)
    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 5

def test_find_connections_in_time_range(sample_log_file):
    graph = build_graph(sample_log_file)
    start_time = "2023-03-15 00:00:00"
    end_time = "2023-03-15 23:59:59"
    connections = find_connections_in_time_range(graph, "HostA", start_time, end_time)
    assert connections['entrantes']['HostC'] == 1
    assert connections['salientes']['HostB'] == 1
    assert connections['salientes']['HostD'] == 1