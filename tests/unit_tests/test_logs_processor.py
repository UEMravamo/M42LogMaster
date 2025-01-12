from os import cpu_count
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from lib.logs_processor import process_chunk_binary, merge_results, process_log_file_binary
from collections import defaultdict
from datetime import datetime
import tempfile



# ---- Pruebas para process_chunk_binary ----

def test_process_chunk_binary_empty_chunk():
    chunk = ""
    init_ = 1629190000
    end_ = 1629190600
    target_host = "host1"

    conns_in, conns_out = process_chunk_binary(chunk, init_, end_, target_host)

    assert conns_in == defaultdict(int)
    assert conns_out == defaultdict(int)


def test_process_chunk_binary_no_target_host():
    chunk = "1629190000000 host1 host2\n1629190300000 host2 host1\n"
    init_ = 1629190000
    end_ = 1629190600
    target_host = "host3"  # Un host que no aparece en el chunk

    conns_in, conns_out = process_chunk_binary(chunk, init_, end_, target_host)

    assert conns_in == defaultdict(int)
    assert conns_out == defaultdict(int)

# ---- Pruebas para merge_results ----

def test_merge_results_empty():
    partial_results = []

    final_results = merge_results(partial_results)

    expected_results = {"entrantes": defaultdict(int), "salientes": defaultdict(int)}

    assert final_results == expected_results

# ---- Pruebas para process_log_file_binary ----

def test_process_log_file_binary_empty_file():
    log_data = ""

    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
        temp_file.write(log_data.encode('utf-8'))
        temp_file.close()

        try:
            results = process_log_file_binary(temp_file.name, init_, end_, target_host, num_workers=cpu_count())
        finally:
            os.remove(temp_file.name)  # Limpiar el archivo temporal

    assert results["entrantes"] == {}
    assert results["salientes"] == {}


def test_process_log_file_binary_with_only_invalid_lines():
    log_data = "invalid line\nanother invalid line\n"

    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
        temp_file.write(log_data.encode('utf-8'))
        temp_file.close()

        try:
            results = process_log_file_binary(temp_file.name, init_, end_, target_host, num_workers=cpu_count())
        finally:
            os.remove(temp_file.name)  # Limpiar el archivo temporal

    assert results["entrantes"] == {}
    assert results["salientes"] == {}


def test_process_log_file_binary_file_not_found():
    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    try:
        results = process_log_file_binary("AAAA.txt", init_, end_, target_host, num_workers=cpu_count())
    except FileNotFoundError:
        pass
    else:
        assert False, "Expected FileNotFoundError"


def test_process_chunk_binary_time_range():
    chunk = """1629190000000 host1 host2
1629190300000 host2 host1
1629190700000 host1 host3"""
    init_ = 1629190000
    end_ = 1629190600
    target_host = "host1"

    conns_in, conns_out = process_chunk_binary(chunk, init_, end_, target_host)

    assert conns_in == {"host2": 1}
    assert conns_out == {"host2": 1, "host3": 1}

def test_merge_results_partial_data():
    partial_results = [
        (defaultdict(int, {"host1": 2}), defaultdict(int, {"host2": 1})),
        (defaultdict(int, {"host3": 1}), defaultdict(int, {"host2": 2}))
    ]

    final_results = merge_results(partial_results)

    expected_results = {
        "entrantes": {"host1": 2, "host3": 1},
        "salientes": {"host2": 3}
    }

    assert final_results == expected_results

def test_process_log_file_binary_large_file():
    log_data = """1629190000000 host1 host2\n""" * 1000  # Repetir línea para simular un archivo grande

    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
        temp_file.write(log_data.encode('utf-8'))
        temp_file.close()

        try:
            results = process_log_file_binary(temp_file.name, init_, end_, target_host, num_workers=cpu_count())
        finally:
            os.remove(temp_file.name)

    assert results["entrantes"] == {}
    assert results["salientes"] == {"host2": 1000}

def test_process_log_file_binary_decoding_error():
    log_data = b"1629190000000 host1 host2\n\xff\xfe\x00\x00"  # Línea inválida

    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
        temp_file.write(log_data)
        temp_file.close()

        try:
            results = process_log_file_binary(temp_file.name, init_, end_, target_host, num_workers=cpu_count())
        finally:
            os.remove(temp_file.name)

    assert results["entrantes"] == {}
    assert results["salientes"] == {"host2": 1}
