from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=2,
    name="El Laberinto",
    story_intro=(
        "El Laberinto de los Condicionales se extiende ante ti.\n"
        "Cada bifurcación es un if, cada recoveco un bucle.\n"
        "Solo quien domine el flujo encontrará la salida."
    ),
    missions=[
        Mission(
            num=1, title="El Guardián",
            description="Escribe un if/else que dado x = 10, muestre 'Par' si es par o 'Impar' si no.",
            execution_mode="script",
            code_template="x = 10\nif x % 2 == 0:\n    print('Par')\nelse:\n    print('Impar')",
            test_cases=[TestCase(input="", expected="Par")],
            hints=["El operador % da el resto de una división", "Usa if/else para bifurcar"],
        ),
        Mission(
            num=2, title="El Bucle Infinito",
            description="Usa un for para mostrar los números del 1 al 5, uno por línea.",
            execution_mode="script",
            code_template="for i in range(1, 6):\n    print(i)",
            test_cases=[TestCase(input="", expected="1\n2\n3\n4\n5")],
            hints=["range(1, 6) genera 1,2,3,4,5", "print() añade salto de línea por defecto"],
        ),
        Mission(
            num=3, title="Comprehension Park",
            description="Usando list comprehension, genera [0, 2, 4, 6, 8] y muéstralo.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="[0, 2, 4, 6, 8]")],
            hints=["[expr for x in iterable] es la sintaxis", "range(0, 9, 2) genera pares"],
        ),
        Mission(
            num=4, title="El Filtro",
            description="Dada la lista nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], muestra solo los pares usando filter o comprehension.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="[2, 4, 6, 8, 10]")],
            hints=["filter(función, lista) filtra elementos", "lambda x: x%2==0 detecta pares"],
        ),
        Mission(
            num=5, title="Boss: FizzBuzz",
            description="Escribe un programa que muestre del 1 al 20, pero:\n- Múltiplos de 3 → 'Fizz'\n- Múltiplos de 5 → 'Buzz'\n- Ambos → 'FizzBuzz'",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="FizzBuzz")],
            hints=["Usa % para detectar múltiplos", "Anida las condiciones: 15 es múltiplo de ambos"],
        ),
    ],
)
