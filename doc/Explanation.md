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
import datetime as dt
from log_processor import preprocess_date, process_log_file_binary, format_connections

if __name__ == "__main__":
    # Fechas de inicio y fin
    init_time = preprocess_date("Martes, 13 de agosto de 2019 01:00:00")
    end_time = preprocess_date("Martes, 13 de agosto de 2019 21:00:00")
    format_ = "%A, %d de %B de %Y %H:%M:%S"
    init_datetime = dt.datetime.strptime(init_time, format_)
    end_datetime = dt.datetime.strptime(end_time, format_)

    # Archivo de logs y host objetivo
    log_file = 'input-file-10000-2.txt'
    host = 'Savhannah'

    try:
        # Procesar el archivo
        results = process_log_file_binary(log_file, init_datetime, end_datetime, host)
        print(format_connections(results, host))
    except FileNotFoundError:
        print(f"Error: El archivo '{log_file}' no existe.")
```

---

## Notas
- Asumimos que el archivo está en `utf-8`.
- El script asume que cada línea tiene: tiempo, host origen y host destino.
- El archivo que se está leyendo es el mismo que hay por defecto pero inflado a 24 millones de líneas.

## TODO's
- [ ] Más manejo de errores.
- [ ] Añadir lo del tiempo de los 5 minutos.
- [ ] Usar PEP8.
---