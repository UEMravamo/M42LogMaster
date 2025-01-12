# LogMaster

Imagina que trabajas para un equipo de ingeniería de redes en una gran empresa tecnológica. Debes diseñar una solución que analice los registros de conexiones entre servidores, identifique patrones de comunicación entre hosts, genere reportes en tiempo real y ayude a comprender el flujo de tráfico en la red.

## Formato del archivo de registro

Cada línea del archivo contiene:
```
<unix_timestamp> <hostname_origen> <hostname_destino>
```
Por ejemplo: 
```
1366815793 quark garak 
1366815795 brunt quark 
1366815811 lilac garak
```


Cada línea representa una conexión desde un host de origen a un host de destino en un momento determinado.

> **Nota**: Las líneas están ordenadas aproximadamente por marca de tiempo, aunque puede haber un desorden de hasta 5 minutos.

---

## Requisitos del Desafío

### 1. Herramienta de Análisis de Logs

Debes implementar una herramienta que procese los archivos de registro (`logfile`) basándose en los siguientes parámetros:

#### Salida esperada
Una lista de los nombres de los hosts conectados al host dado dentro del período especificado.

#### Ejemplo de entrada de prueba

- **init_datetime**: Martes, 13 de agosto de 2019 01:00:00  
- **end_datetime**: Martes, 13 de agosto de 2019 21:00:00  
- **Hostname**: Savhannah  

#### Parámetros de entrada

1. Nombre del archivo (por ejemplo: `input-file-10000.txt`).
2. Fecha y hora de inicio (`init_datetime`).
3. Fecha y hora de fin (`end_datetime`).
4. Nombre del host (`hostname`).

---

### 2. Modo en Tiempo Real

La herramienta debe ser capaz de procesar:

- Archivos de registro existentes.
- Nuevos registros mientras el archivo se escribe.

En este modo, la herramienta debe emitir cada hora:

1. Los hostnames conectados al host configurado en la última hora.
2. Los hostnames que recibieron conexiones del host configurado en la última hora.
3. El hostname que generó más conexiones en la última hora.

---

## Consideraciones de Implementación

- El número de líneas en el archivo y la cantidad de nombres de host pueden ser **muy grandes**.
- La solución debe ser eficiente en términos de uso de **CPU y memoria**.
- Puedes hacer suposiciones razonables, pero deben estar **claramente documentadas**.

---
## Requisitos
- Usa Python 3.7. o superior
- Escribe código conforme a PEP8.
- Escribe algunas pruebas (considera usar pytest o uniitest).
- Documenta tu solución en un archivo.
  
---
  ## Estructura del proyecto 
```
LogMaster/
├── .idea/                                
├── data/                                   
│   ├── input-file-10000.txt                # Dataset original de logs
│   └── file_generator.py                   # Script para crear datasets aleatorios de prueba con cierta longitud  
├── lib/                                    
│   ├── file_manager.py                     # Librería para la gestión de inputs y outputs de la app
│   └── log_processor.py                    # Librería para procesamiento y análisis de logs
├── scripts/                                
│   ├── last_hour_log_processor.py          # Script para generar resumen de conexiones en la última hora
│   └── LogMaster.py                        # Script para listar conexiones de un host en un rango de tiempo
├── tests/
│   ├── unit_tests/                         # Pruebas unitarias de las funciones de la aplicación
│   ├── resource_usage_tests/               # Pruebas para medir el uso de recursos como CPU y memoria
│   └── performance_tests/                  # Pruebas de rendimiento para evaluar la eficiencia (tiempos de ejecución) de las funciones de la aplicación
├── .gitignore                             
└── README.md

```

## Documentación
Puedes acceder a la documentación completa del proyecto [aquí](https://docs.google.com/document/d/1vvBf8FPUfStvpJqVeKR10krPRe5Z5PtCnuP5KiehfOc/edit?usp=sharing).

## Presentación
Consulta la presentación del proyecto en Canva [aquí](https://docs.google.com/presentation/d/1wrV6Ooe8k7wmccb6YEOVrjVAIGUhozd4/edit?usp=sharing&ouid=113986353646284854490&rtpof=true&sd=true).
