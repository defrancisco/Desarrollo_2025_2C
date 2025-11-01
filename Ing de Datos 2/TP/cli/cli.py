import os
import sys
from rich.console import Console
from rich.table import Table

console = Console()
QUERIES_DIR = "/app/queries"

# Mapeo de extensión a comando de ejecución y alias de DB
EXECUTOR_MAP = {
    ".sql": {
        "cmd": "mysql  -h mysql -u root -proot_password my_data_warehouse --batch --table --skip-ssl < {file}",
        "db": "MySQL"
    },
    ".js": {
        "cmd": "mongosh mongodb://mongodb:27017/starbucks_transactions -u rootuser -p rootpassword --authenticationDatabase admin --file {file} --quiet",
        "db": "MongoDB"
    },
    ".cql": {
        "cmd": "cqlsh cassandra -f {file}",
        "db": "Cassandra"
    },
    ".cypher": {
    "cmd": "QUERY=$(cat {file}); printf '{{\"statements\": [{{ \"statement\": \"%s\" }}]}}' \"$QUERY\" | curl -s -X POST -H 'Content-Type: application/json' -u neo4j:neo4jpassword 'http://neo4j:7474/db/neo4j/tx/commit' -d @-",
    "db": "Neo4j"
    },

    ".py": {"cmd": "python {file}", "db": "Python File"},
    ".sh": {
        # Usamos 'sh {file}' para ejecutar el script completo.
        "cmd": "sh {file}", 
        "db": "Políglota" 
    },
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_tui():
    clear_screen()
    
    # 1. Cargar Scripts
    try:
        scripts = sorted([f for f in os.listdir(QUERIES_DIR) if os.path.isfile(os.path.join(QUERIES_DIR, f))])
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] Directorio de consultas no encontrado en /app/queries.")
        return

    while True:
        clear_screen()
        console.print("[bold cyan]☕ Starbucks Políglota - Consola de Ejecución 🚀[/bold cyan]\n")

        # 2. Mostrar Tabla de Opciones
        table = Table(title="Scripts de Consulta Disponibles", show_lines=True)
        table.add_column("ID", style="dim", width=4)
        table.add_column("Script", style="bold green")
        table.add_column("Base de Datos", style="yellow")
        
        for i, script_name in enumerate(scripts):
            ext = os.path.splitext(script_name)[1]
            db_alias = EXECUTOR_MAP.get(ext, {}).get("db", "Desconocida")
            table.add_row(str(i + 1), script_name, db_alias)

        console.print(table)
        console.print("\n[bold]Escriba el ID del script para ejecutar, o 'q' para salir.[/bold]")

        # 3. Leer la Selección
        choice = console.input("Selección: ").strip()

        if choice.lower() == 'q':
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(scripts):
                selected_script = scripts[index]
                ext = os.path.splitext(selected_script)[1]
                executor = EXECUTOR_MAP.get(ext)
                
                if executor:
                    full_path = os.path.join(QUERIES_DIR, selected_script)
                    command = executor["cmd"].format(file=full_path)
                    
                    console.print(f"\n[bold blue]>>> Ejecutando {selected_script} en {executor['db']}...[/bold blue]")
                    # debug
                    print(command)
                    # Ejecutar el comando en el shell del contenedor
                    os.system(command) 
                    
                    console.input("\n[bold yellow]Presione ENTER para continuar...[/bold yellow]")
                else:
                    console.print("[bold red]Error:[/bold red] Extensión de archivo no soportada.")
            else:
                console.print("[bold red]Error:[/bold red] ID no válido.")
        except ValueError:
            console.print("[bold red]Error:[/bold red] Por favor, ingrese un número o 'q'.")
        except Exception as e:
            console.print(f"[bold red]Error de ejecución:[/bold red] {e}")

    console.print("[bold green]¡Saliendo de la TUI! Hasta pronto. 👋[/bold green]")


if __name__ == "__main__":
    run_tui()