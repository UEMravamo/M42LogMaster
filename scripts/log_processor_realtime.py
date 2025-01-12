import sys
import os
import time
from datetime import datetime, timedelta
import networkx as nx

#Ruta a log
ruta_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/input-file-10000.txt'))

def crear_grafo_filtrado(log_file, tiempo_inicio, tiempo_fin):
    G = nx.DiGraph()
    try:
        with open(log_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                timestamp = int(parts[0]) // 1000
                timestamp_datetime = datetime.utcfromtimestamp(timestamp)
                host_from = parts[1]
                host_to = parts[2]

                #Filtrar por tiempo
                if tiempo_inicio <= timestamp_datetime <= tiempo_fin:
                    if not G.has_node(host_from):
                        G.add_node(host_from)
                    if not G.has_node(host_to):
                        G.add_node(host_to)
                    G.add_edge(host_from, host_to, timestamp=timestamp_datetime)

    except Exception as e:
        print(f"Error: {e}")
    return G

def analisis_tiempo_real():
    print("Empezar análisis")
    tiempo_inicio = datetime.now()
    una_hora = tiempo_inicio - timedelta(hours=1)
    #Сrear grafo 
    grafo = crear_grafo_filtrado(ruta_log, una_hora, tiempo_inicio)

    #Estadistica
    estadistica = {}
    for node in grafo.nodes():
        entradas = grafo.in_degree(node)
        salidas = grafo.out_degree(node)

        if entradas > 0 or salidas > 0:
            estadistica[node] = {'entrantes': entradas, 'salientes': salidas}

    #Si no hay conexiones
    if not estadistica:
        print("No hay conexiones la ultima hora.")
        return

    #Print estadistica
    print("Estadistica de la ultima hora:")
    for host, datos in estadistica.items():
        print(f"Host: {host}")
        print(f"  Entrantes: {datos['entrantes']}")
        print(f"  Salientes: {datos['salientes']}")

    #Host con conexiones maximas
    conexiones_maximos = max(
        estadistica,
        key=lambda host: estadistica[host]['entrantes'] + estadistica[host]['salientes']
    )
    print(f"Host con conexiones maximas: {conexiones_maximos}")
    print("Fin de analisis")

if __name__ == "__main__":
    while True:
        analisis_tiempo_real()
        time.sleep(3600)