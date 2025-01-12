#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
from io import StringIO
# función para procesar los logs
def process_logs(file_path, start_ts, end_ts, target_host):

    connections = set()

    with open(file_path, 'r') as log_file:
        for line in log_file:
            ts, src, dest = line.strip().split()
            ts = int(ts) // 1000 #milisegundos a segundos
            if start_ts <= ts <= end_ts:
                if src == target_host:
                    connections.add(dest)
                elif dest == target_host:
                    connections.add(src)
    return connections


# Parámetros de entrada
file_path = "C:/Users/34633/Desktop/input-file-10000.txt"
start_ts = 1565647228897 // 1000
end_ts = 1665700962726 // 1000
target_host = "Heera"

# Procesar los logs y obtener los resultados
connected_hosts = process_logs(file_path, start_ts, end_ts, target_host)

# Imprimir el resultado
print(f"Hosts conectados a '{target_host}' entre {datetime.datetime.fromtimestamp(start_ts)} y {datetime.datetime.fromtimestamp(end_ts)}:")
for host in connected_hosts:
    print(host)
def run_tests():
    try:
        # Test 1: Verificar que el archivo no esté vacío
        try:
            process_logs(file_path, start_ts, end_ts, target_host)
            print("Test 1: El archivo no esta vacio")
        except ValueError as e:
            print("Test 1: El archivo esta vacio")
        
        # Test 2: Verificar que el rango temporal sea válido
        try:
            process_logs(file_path, end_ts, start_ts, target_host)
            print("Test 2: El rango temporal no es valido")
        except ValueError as e:
            print("Test 2: El rango temporal es adecuado")

        # Test 3: Verificar que el host objetivo exista
        try:
            non_existent_host = "NonExistentHost"
            result = process_logs(file_path, start_ts, end_ts, non_existent_host)
            if not result:
                print("Test 3: El host existe")
            else:
                print("Test 3: El host es incorrecto")
        except ValueError as e:
            print("Test 3: El host es inexistente")

        # Test 4: Verificar que el formato de entrada sea válido
        try:
            process_logs(file_path, start_ts, end_ts, target_host)
            print("Test 4: Formato de entrada valido")
        except ValueError as e:
            print(f"Test 4: Formato de entrada invalido")

    except Exception as e:
        print(f"Error inesperado durante las pruebas: {e}")

# Ejecutar pruebas
run_tests()


# In[ ]:




