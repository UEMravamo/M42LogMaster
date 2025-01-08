# Procesar los registros de la última hora y crear estadísticas

# Obtener hostnames conectados al host configurado en la última hora.
# Obtener hostnames que recibieron conexiones del host configurado en la última hora.
# Obtener hostname que generó más conexiones en la última hora.
import sys
import os
import time
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.log_procesor import build_graph, find_connections_in_time_range

#Ruta a log
ruta_log = '../data/input-file-10000.txt'

def analisis_tiempo_real():
    #Analizar cada hora
    print("Empezar análisis")
    #Сrear grafo
    grafo = build_graph(ruta_log)
    #Tiempo
    tiempo_inicio = datetime.now()
    una_hora = tiempo_inicio - timedelta(hours=1)
    
    #Estadistica
    estadistica = {}
    for node in grafo.nodes():
        conexiones = find_connections_in_time_range(grafo, node, una_hora, tiempo_inicio)
        print(f"Conexiones para {node}: {conexiones}")
        estadistica[node] = {
            'entrantes': sum(conexiones['entrantes'].values()),
            'salientes': sum(conexiones['salientes'].values())
        }
    
    #Print los datos
    conexiones_maximos = max(
        estadistica,
        key=lambda host: estadistica[host]['entrantes'] + estadistica[host]['salientes']
    )
    
    print("Estadistica de la ultima hora:")
    for host, estadistica in estadistica.items():
        print(f"Host: {host}")
        print(f"  Entrantes: {estadistica['entrantes']}")
        print(f"  Salientes: {estadistica['salientes']}")
    
    print(f"Host con conexiones maximas: {conexiones_maximos}")
    print("Fin de analisis")

if __name__ == "__main__":
    while True:
        analisis_tiempo_real()
        time.sleep(3600)