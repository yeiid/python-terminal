from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=6,
    name="El Puerto",
    story_intro=(
        "En el Puerto de los Módulos atracan barcos de todo tipo.\n"
        "Importar y exportar es el pan de cada día.\n"
        "El contramaestre te pide que organices la carga."
    ),
    missions=[
        Mission(
            num=1, title="Importar el Necesario",
            description="Importa el módulo `math` y muestra el valor de pi (math.pi) con 4 decimales.",
            execution_mode="script",
            code_template="import math\nprint(f'{math.pi:.4f}')",
            test_cases=[TestCase(input="", expected="3.1416")],
            hints=["import math importa el módulo", "math.pi tiene el valor de π"],
        ),
        Mission(
            num=2, title="Alias y Navegación",
            description="Importa `datetime` como `dt` y muestra el año actual con dt.date.today().year.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="2026")],
            hints=["import datetime as dt crea un alias", "dt.date.today().year da el año actual"],
        ),
        Mission(
            num=3, title="Solo lo Necesario",
            description="Importa solo `sqrt` y `pow` de math. Muestra sqrt(16) y pow(2, 10).",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="4.0")],
            hints=["from math import sqrt, pow importa solo esas funciones", "pow(2, 10) = 1024"],
        ),
        Mission(
            num=4, title="Tu Propio Módulo",
            description="Escribe un script que cree un archivo `utilidades.py` con una función `saludar(nombre)`, luego importe dinámicamente el módulo (importlib) y use la función.",
            execution_mode="script",
            code_template="import importlib.util\nimport sys\n\ncodigo = '''def saludar(nombre):\\n    return f\"Hola {nombre}!\"'''\n\nwith open('utilidades.py', 'w') as f:\n    f.write(codigo)\n\nspec = importlib.util.spec_from_file_location('utilidades', 'utilidades.py')\nmod = importlib.util.module_from_spec(spec)\nsys.modules['utilidades'] = mod\nspec.loader.exec_module(mod)\n\nprint(mod.saludar('Mundo'))",
            test_cases=[TestCase(input="", expected="Hola Mundo!")],
            hints=["importlib permite importar dinámicamente", "spec_from_file_location y exec_module"],
        ),
        Mission(
            num=5, title="Boss: Explorador de Módulos",
            description="Usa `math` y muestra todas las funciones que contiene usando dir(). Filtra las que NO empiezan con '_' y muéstralas ordenadas.",
            execution_mode="script",
            code_template="import math\n\nfuncs = [f for f in dir(math) if not f.startswith('_')]\nfor f in sorted(funcs):\n    print(f)",
            test_cases=[TestCase(input="", expected="acos")],
            hints=["dir(math) lista todo del módulo", "Filtra con list comprehension y not f.startswith('_')"],
        ),
    ],
)
