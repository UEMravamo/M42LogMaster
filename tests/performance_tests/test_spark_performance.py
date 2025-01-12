# tests/test_performance.py
import pytest
import time
from lib.logs_processor import process_log_file_binary, process_log_spark
from pyspark.sql import SparkSession

@pytest.fixture(scope="module")
def spark_session():
    spark = SparkSession.builder \
        .appName("LogProcessorTest") \
        .master("local[*]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture(scope="module")
def large_log_file(tmpdir_factory):
    log_file = tmpdir_factory.mktemp("data").join("large_log.txt")
    with open(log_file, 'w') as f:
        for i in range(10000):  # Ajusta el tamaño según sea necesario
            f.write(f"16788864{i:04} HostA HostB\n")
    return str(log_file)

def test_process_log_file_binary_performance(large_log_file):
    start_time = time.time()
    process_log_file_binary(large_log_file, start_datetime=datetime.now() - timedelta(minutes=5), end_datetime=datetime.now(), target_host="HostA")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nprocess_log_file_binary execution time: {elapsed_time:.4f} seconds")
    assert elapsed_time < 5  # Define un límite de tiempo razonable

def test_process_log_spark_performance(spark_session, large_log_file):
    start_time = time.time()
    process_log_spark(large_log_file, "HostA", "2023-03-15 00:00:00", "2023-03-15 23:59:59")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nprocess_log_spark execution time: {elapsed_time:.4f} seconds")
    assert elapsed_time < 5  # Define un límite de tiempo razonable