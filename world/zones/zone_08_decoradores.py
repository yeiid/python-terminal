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
            description="Crea un decorador `registro` que muestre 'Iniciando <nombre_func>' al empezar y 'Finalizado <nombre_func>' al terminar. Decora una función `saludar()` que haga print('Hola!').",
            execution_mode="script",
            code_template="def registro(func):\n    def wrapper(*args, **kwargs):\n        print(f'Iniciando {func.__name__}')\n        resultado = func(*args, **kwargs)\n        print(f'Finalizado {func.__name__}')\n        return resultado\n    return wrapper\n\n@registro\ndef saludar():\n    print('Hola!')\n\nsaludar()",
            test_cases=[TestCase(input="", expected="Iniciando saludar\nHola!\nFinalizado saludar")],
            hints=["func.__name__ da el nombre de la función", "El wrapper debe llamar a func() entre los prints"],
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
            description="Crea un decorador `validar_positivos` que verifique que todos los argumentos numéricos sean > 0. Si alguno es <= 0, lanza ValueError. Prueba con dividir(10, 2) que debe funcionar.",
            execution_mode="script",
            code_template="def validar_positivos(func):\n    def wrapper(*args, **kwargs):\n        for arg in args:\n            if isinstance(arg, (int, float)) and arg <= 0:\n                raise ValueError('Argumento debe ser positivo')\n        return func(*args, **kwargs)\n    return wrapper\n\n@validar_positivos\ndef dividir(a, b):\n    return a / b\n\nprint(dividir(10, 2))",
            test_cases=[TestCase(input="", expected="5.0")],
            hints=["Inspecciona args con *args, **kwargs", "isinstance(arg, (int, float)) verifica si es número"],
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
