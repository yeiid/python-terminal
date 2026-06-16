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
            description="Importa `datetime` como `dt` y muestra la fecha actual con dt.date.today().",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["import datetime as dt crea un alias", "dt.date.today() da la fecha actual"],
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
            description="Crea un módulo `utilidades.py` con una función `saludar(nombre)`. En otro script, impórtalo y úsalo.\n(Escribe solo el script principal.)",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["from utilidades import saludar", "El módulo debe estar en el mismo directorio"],
        ),
        Mission(
            num=5, title="Boss: Explorador de Módulos",
            description="Usa `importlib` o `pkgutil` para listar todos los submódulos de `collections`. Muestra la lista ordenada.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["pkgutil.iter_modules() lista submódulos", "sorted() ordena la lista alfabéticamente"],
        ),
    ],
)
