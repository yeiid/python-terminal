from world.zones import Zone, Mission


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
            validation_fn=lambda out, err: (out == "HOLA", "Debe mostrar 'HOLA'"),
        ),
        Mission(
            num=2, title="Temporizador",
            description="Crea un decorador `tiempo` que mida y muestre los segundos que tarda una función en ejecutarse. Decora una función que suma 1e6 números.",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=3, title="Contador de llamadas",
            description="Usa functools.wraps y crea un decorador `contador` que lleve la cuenta de cuántas veces se llamó a la función. Llámala 3 veces y muestra el contador.",
            validation_fn=lambda out, err: ("3" in out, "Debe mostrar 3 llamadas"),
        ),
        Mission(
            num=4, title="Validación de Argumentos",
            description="Crea un decorador `validar_positivos` que verifique que todos los argumentos numéricos sean > 0. Si no, lanza ValueError. Prueba con una función que divide.",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=5, title="Boss: Cache Decorator",
            description="Implementa un decorador `cache` que almacene resultados de llamadas anteriores (memoización). Decora `fibonacci(n)` recursivo y calcula fib(35).",
            validation_fn=lambda out, err: ("9227465" in out, "fib(35) = 9227465"),
        ),
    ],
)
