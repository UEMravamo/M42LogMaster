import random
from datetime import datetime, timedelta
import os

def generate_large_log(file_name, num_lines):
    start_time = datetime.now()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "w") as f:
        for _ in range(num_lines):
            timestamp = int((start_time + timedelta(seconds=random.randint(0, 100000))).timestamp() * 1000)
            host_from = f"Host{random.randint(1, 100)}"
            host_to = f"Host{random.randint(1, 100)}"
            f.write(f"{timestamp} {host_from} {host_to}\n")

# Generar archivo
generate_large_log("large_log_test.txt", 5_000_000)