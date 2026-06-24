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
            description="Usa el módulo os para mostrar el directorio actual (getcwd()) y cuenta cuántos archivos .py hay en él (listdir y filter).",
            execution_mode="script",
            code_template="import os\n\ncwd = os.getcwd()\narchivos = os.listdir('.')\npy_count = len([f for f in archivos if f.endswith('.py')])\n\nprint(f'Dir: {cwd}')\nprint(f'Archivos .py: {py_count}')",
            test_cases=[TestCase(input="", expected=".py")],
            hints=["os.getcwd() da el directorio actual", "os.listdir('.') lista los archivos"],
        ),
        Mission(
            num=2, title="Argumentos de Línea",
            description="Simula argparse: usa `input()` para recibir argumentos en formato `--nombre <valor> --edad <valor>` y parsea manualmente. Muestra 'Hola NOMBRE, tienes EDAD años'.",
            execution_mode="script",
            code_template="args_str = input()\npartes = args_str.split()\nnombre = partes[partes.index('--nombre') + 1] if '--nombre' in partes else 'Desconocido'\nedad = partes[partes.index('--edad') + 1] if '--edad' in partes else '?'\n\nprint(f'Hola {nombre}, tienes {edad} años')",
            test_cases=[TestCase(input="--nombre Ana --edad 28", expected="Hola Ana, tienes 28 años")],
            hints=["input() recibe una línea completa", "str.split() separa por espacios"],
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
                "Crea un parser manual que reciba por input() un comando:\n"
                "- 'suma a b' → muestra la suma\n"
                "- 'multiplica a b' → muestra el producto\n"
                "- 'archivo ruta' → lee y muestra el archivo\n"
                "Prueba con: suma 5 7"
            ),
            execution_mode="script",
            code_template="cmd = input().split()\naccion = cmd[0]\n\nif accion == 'suma':\n    a, b = int(cmd[1]), int(cmd[2])\n    print(a + b)\nelif accion == 'multiplica':\n    a, b = int(cmd[1]), int(cmd[2])\n    print(a * b)\nelif accion == 'archivo':\n    with open(cmd[1], 'r') as f:\n        print(f.read())\nelse:\n    print('Comando desconocido')",
            test_cases=[TestCase(input="suma 5 7", expected="12")],
            hints=["input().split() separa el comando en partes", "int() convierte a entero"],
        ),
    ],
)
