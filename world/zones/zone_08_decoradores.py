from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=8,
    name="El Templo",
    story_intro=(
        "El Templo de los Decoradores resplandece con luz propia.\n"
        "Los monjes envuelven funciones con capas de poder.\n"
        "El maestro te enseña el arte de la metaprogramación."
    ),
    missions=[
        Mission(
            num=1, title="La Capa Simple",
            description="Define un decorador `mayusculas` que convierta el resultado de una función a mayúsculas. Decora `saludar()` que retorna 'hola' y muéstralo.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="HOLA")],
            hints=["Un decorador envuelve una función", "resultado.upper() convierte a mayúsculas"],
        ),
        Mission(
            num=2, title="Temporizador",
            description="Crea un decorador `tiempo` que mida y muestre los segundos que tarda una función en ejecutarse. Decora una función que suma 1e6 números.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["time.time() da el tiempo actual en segundos", "Resta el tiempo inicial al final"],
        ),
        Mission(
            num=3, title="Contador de llamadas",
            description="Usa functools.wraps y crea un decorador `contador` que lleve la cuenta de cuántas veces se llamó a la función. Llámala 3 veces y muestra el contador.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="3")],
            hints=["functools.wraps preserva los metadatos", "Un contador se almacena como atributo de la función"],
        ),
        Mission(
            num=4, title="Validación de Argumentos",
            description="Crea un decorador `validar_positivos` que verifique que todos los argumentos numéricos sean > 0. Si no, lanza ValueError. Prueba con una función que divide.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["Inspecciona args con *args, **kwargs", "raise ValueError('mensaje') lanza la excepción"],
        ),
        Mission(
            num=5, title="Boss: Cache Decorator",
            description="Implementa un decorador `cache` que almacene resultados de llamadas anteriores (memoización). Decora `fibonacci(n)` recursivo y calcula fib(35).",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="9227465")],
            hints=["Usa un dict para cachear resultados", "if n in cache: return cache[n]"],
        ),
    ],
)
