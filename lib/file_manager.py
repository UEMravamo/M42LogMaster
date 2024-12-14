# Librería para la gestión y carga de archivos de log

def preprocess_date(date_str):
    """Convierte nombres de días y meses en español a inglés directamente(no me funciona la librería locale)."""
    return (date_str
            .replace("Lunes", "Monday").replace("Martes", "Tuesday")
            .replace("Miércoles", "Wednesday").replace("Jueves", "Thursday")
            .replace("Viernes", "Friday").replace("Sábado", "Saturday")
            .replace("Domingo", "Sunday")
            .replace("enero", "January").replace("febrero", "February")
            .replace("marzo", "March").replace("abril", "April")
            .replace("mayo", "May").replace("junio", "June")
            .replace("julio", "July").replace("agosto", "August")
            .replace("septiembre", "September").replace("octubre", "October")
            .replace("noviembre", "November").replace("diciembre", "December"))

# Generar el output
def format_connections(conns, server_name):
    """Formatea el output para ver el número de conexiones por host."""
    formatted = [f"Conexiones del servidor: {server_name}"]
    for direction, hosts in conns.items():
        formatted.append(f"Conexiones {direction}:")
        for host_, count in hosts.items():
            formatted.append(f"  - {host_}: {count} conexiones ")
    return '\n'.join(formatted)