import os
import sys
import time
import tempfile
from datetime import datetime
from os import cpu_count

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from lib.logs_processor import process_chunk_binary, merge_results, process_log_file_binary

def test_process_log_file_binary_performance():
    """Prueba de rendimiento para un archivo grande."""
    log_data = """1629190000000 host1 host2\n""" * 100000

    init_ = datetime.fromtimestamp(1629190000)
    end_ = datetime.fromtimestamp(1629190600)
    target_host = "host1"

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
        temp_file.write(log_data.encode('utf-8'))
        temp_file.close()

        start_time = time.time()
        try:
            results = process_log_file_binary(temp_file.name, init_, end_, target_host, num_workers=cpu_count())
        finally:
            os.remove(temp_file.name)

        end_time = time.time()

        print("Resultados obtenidos:", results)
        print("Tiempo de ejecución:", end_time - start_time, "segundos")

        assert results["salientes"] == {"host2": 100000}
        assert (end_time - start_time) < 5, "El procesamiento tardó más de 5 segundos"

def run_test_performance():
    try:
        test_process_log_file_binary_performance()
        print("test_process_log_file_binary_performance: PASSED")
    except AssertionError as e:
        print(f"test_process_log_file_binary_performance: FAILED - {str(e)}")
    except Exception as e:
        print(f"test_process_log_file_binary_performance: FAILED with unexpected error - {str(e)}")

if __name__ == "__main__":
    run_test_performance()
