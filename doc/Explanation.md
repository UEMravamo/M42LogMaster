# Explicación del Código

---

## Resumen General
El script analiza archivos de logs para contar:
- **Conexiones entrantes** hacia un host objetivo.
- **Conexiones salientes** desde ese host.

Lo hace dentro de un rango de tiempo específico y divide el archivo en fragmentos para procesarlos en paralelo, leyéndolo en binario y luego decodificándolo y procesándolo.

---

## Funciones Principales

### `preprocess_date`
 Esto es porque `datetime` no soporta las fechas en español y no he podido usar `locale`, convierte una fecha escrita en español (como "Martes, 13 de agosto de 2019") a un formato procesable. 

- **Entrada:** Una fecha en español.
- **Salida:** La misma fecha traducida al inglés.

---

### `process_chunk_binary`
Cuenta las conexiones en un fragmento del archivo de logs.

1. **Entrada:**
   - Un fragmento del archivo (texto).
   - Rango de tiempo (inicio y fin en formato UNIX).
   - Host objetivo.
2. **Salida:**
   - Número de conexiones entrantes y salientes hacia/desde el host objetivo.
3. **Qué hace:**
   - Divide el fragmento en líneas.
   - Extrae la información de cada línea (tiempo, host origen y host destino).
   - Cuenta las conexiones dentro del rango de tiempo.

---

### `merge_results`
Combina los resultados de los fragmentos.

- **Entrada:** Resultados de cada fragmento.
- **Salida:** Un resultado final con las conexiones de todos los fragmentos.

---

### `process_log_file_binary`
Procesa todo el archivo de logs.

1. **Entrada:**
   - Ruta del archivo.
   - Rango de tiempo.
   - Host objetivo.
   - Número de procesos (opcional).
2. **Salida:**
   - Cuenta de todas las conexiones.
3. **Qué hace:**
   - Divide el archivo en fragmentos pequeños (1 MB).
   - Procesa cada fragmento en paralelo.
   - Combina los resultados.
> **Nota (leftover):** El usar el leftover es para evitar que se pierda información en el caso de que un fragmento (1 MB) termine en medio de una línea y se pierda parte de la información.


---

### `format_connections`
Formatea los resultados de las conexiones.

- **Entrada:**
   - Resultados de las conexiones.
   - Nombre del servidor analizado.
- **Salida:**
   - Un texto con las conexiones entrantes y salientes organizadas.

---

## Ejemplo de Uso
```python
# Script para listar conexiones de un host en un periodo de tiempo

import datetime as dt
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.file_manager import preprocess_date, format_connections
from lib.logs_processor import process_log_file_binary

if __name__ == "__main__":
    # Cronómetro de inicio
    start = time.time()

    # Configuración de variables
    log_file = '../data/input-file-10000-2.txt'
    host = 'Savhannah'
    init_datetime_str = "Martes, 13 de agosto de 2019 01:00:00"
    end_datetime_str = "Martes, 13 de agosto de 2019 21:00:00"
    datetime_format = "%A, %d de %B de %Y %H:%M:%S"

    # Validar el archivo
    if not os.path.exists(log_file):
        print(f"Error: El archivo '{log_file}' no existe.")
        sys.exit(1)

    # Validar el host
    if not isinstance(host, str) or not host.strip():
        print("Error: El valor del host no es válido. Debe ser una cadena no vacía.")
        sys.exit(1)

    # Preprocesar y validar fechas
    try:
        init_datetime_str = preprocess_date(init_datetime_str)
        end_datetime_str = preprocess_date(end_datetime_str)
        init_datetime = dt.datetime.strptime(init_datetime_str, datetime_format)
        end_datetime = dt.datetime.strptime(end_datetime_str, datetime_format)

        if init_datetime >= end_datetime:
            raise ValueError("La fecha inicial debe ser anterior a la fecha final.")
    except ValueError as e:
        print(f"Error en la configuración de fechas: {e}")
        sys.exit(1)

    # Procesar conexiones
    try:
        connections = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(connections, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")
    except Exception as e:
        print(f"Error inesperado durante el procesamiento de conexiones: {e}")

    # Cronómetro de fin
    end = time.time()
    print(f"Tiempo total de ejecución: {end - start:.10f} segundos ")

```

---

## Notas
- Asumimos que el archivo está en `utf-8`.
- El script asume que cada línea tiene: tiempo, host origen y host destino.
- El archivo que se está leyendo es el mismo que hay por defecto pero inflado a 24 millones de líneas.
- Se puede cambiar el archivo de logs en la variable `log_file`.
- Se puede cambiar el host objetivo en la variable `host`.
- Se puede cambiar el rango de tiempo en las variables `init_datetime_str` y `end_datetime_str`.
---