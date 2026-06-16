from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=12,
    name="El Cuartel",
    story_intro=(
        "El Cuartel General es el centro de operaciones.\n"
        "Aquí se manejan las herramientas del sistema.\n"
        "El comandante te asigna misiones del mundo real."
    ),
    missions=[
        Mission(
            num=1, title="OS Explorer",
            description="Usa el módulo os para mostrar el directorio actual (getcwd()) y listar los archivos (listdir('.')).",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["os.getcwd() da el directorio actual", "os.listdir('.') lista los archivos"],
        ),
        Mission(
            num=2, title="Argumentos de Línea",
            description="Usa argparse para crear un programa que acepte --nombre y --edad y muestre 'Hola NOMBRE, tienes EDAD años'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["import argparse y ArgumentParser", "parser.add_argument('--nombre') añade opción"],
        ),
        Mission(
            num=3, title="Subprocess Power",
            description="Usa subprocess.run() para ejecutar 'echo Hola desde subprocess' y captura/muestra la salida.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="Hola desde subprocess")],
            hints=["subprocess.run(['echo', '...'], capture_output=True)", "result.stdout captura la salida"],
        ),
        Mission(
            num=4, title="Solicitud HTTP",
            description="Usa urllib.request o requests (si está instalado) para hacer GET a 'https://httpbin.org/get' y mostrar el status code.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="200")],
            hints=["urllib.request.urlopen('url') hace GET", "response.status da el código de estado"],
        ),
        Mission(
            num=5, title="Boss: CLI Definitiva",
            description=(
                "Crea una CLI completa con argparse que:\n"
                "- Acepte un comando: 'suma', 'multiplica', 'archivo'\n"
                "- Para suma: --a --b (enteros)\n"
                "- Para multiplica: --a --b (enteros)\n"
                "- Para archivo: --ruta (lee y muestra el archivo)\n"
                "Prueba con suma 5 7."
            ),
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["add_subparsers() para múltiples comandos", "type=int para argumentos enteros"],
        ),
    ],
)
