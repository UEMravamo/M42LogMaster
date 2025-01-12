#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import psutil
import time

# Definir la función para procesar los logs
def process_logs(file_path, start_ts, end_ts, target_host):
    connections = set()

    with open(file_path, 'r') as log_file:
        for line in log_file:
            ts, src, dest = line.strip().split()
            ts = int(ts) // 1000  # Convertir de milisegundos a segundos
            if start_ts <= ts <= end_ts:
                if src == target_host:
                    connections.add(dest)
                elif dest == target_host:
                    connections.add(src)
    return connections


# Función para monitorear el rendimiento y el uso de recursos
def monitor_performance(func, *args, **kwargs):
    process = psutil.Process()
    
    # Medir memoria inicial
    start_memory = process.memory_info().rss / 1024 / 1024  # Memoria inicial en MB
    start_cpu = process.cpu_percent(interval=None)  # Uso inicial de CPU
    
    # Medir tiempo de ejecución
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    # Medir memoria y CPU final
    end_memory = process.memory_info().rss / 1024 / 1024  # Memoria final en MB
    end_cpu = process.cpu_percent(interval=None)  # Uso final de CPU

    # Mostrar resultados
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
    print(f"Memoria usada: {end_memory - start_memory:.2f} MB")
    print(f"CPU usada: {end_cpu}%")
    
    return result


# Parámetros de entrada
file_path = "C:/Users/34633/Desktop/input-file-10000.txt"
start_ts = 1565647228897 // 1000  # Convertir de milisegundos a segundos
end_ts = 1665700962726 // 1000   # Convertir de milisegundos a segundos
target_host = "Heera"

# Ejecutar la función con monitoreo de rendimiento y recursos
connected_hosts = monitor_performance(process_logs, file_path, start_ts, end_ts, target_host)

# Imprimir el resultado
print(f"Hosts conectados a '{target_host}' entre {datetime.datetime.fromtimestamp(start_ts)} y {datetime.datetime.fromtimestamp(end_ts)}:")
for host in connected_hosts:
    print(host)


# In[ ]:




