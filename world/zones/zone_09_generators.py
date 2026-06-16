from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=9,
    name="El Río",
    story_intro=(
        "El Río de los Generadores fluye sin detenerse.\n"
        "Sus aguas llevan datos que solo se revelan al avanzar.\n"
        "La guardiana del río te reta a domar la corriente."
    ),
    missions=[
        Mission(
            num=1, title="Primer Generator",
            description="Escribe un generator `contar(n)` que yield del 1 al n. Úsalo con for para mostrar los números.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="1, 2, 3, 4, 5")],
            hints=["yield produce un valor y pausa la función", "Usa for num in contar(5): para iterar"],
        ),
        Mission(
            num=2, title="Yield From",
            description="Usa `yield from` para aplanar una lista de listas: [[1,2], [3,4], [5,6]] y mostrar los elementos.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="1\n2\n3\n4\n5\n6")],
            hints=["yield from aplana una sublista", "Sustituye un for anidado"],
        ),
        Mission(
            num=3, title="Infinito Controlado",
            description="Crea un generator `pares()` que genere números pares infinitamente. Toma los primeros 10 con un bucle y break.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="0\n2\n4\n6\n8\n10\n12\n14\n16\n18")],
            hints=["while True genera infinitamente", "break sale del bucle cuando quieras"],
        ),
        Mission(
            num=4, title="Pipeline Generator",
            description="Crea dos generators: `cuadrados(nums)` que eleve al cuadrado, y `mostrar(nums)` que imprima. Conéctalos en pipeline: range(1, 6) -> cuadrados -> mostrar.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="1\n4\n9\n16\n25")],
            hints=["Los generators se pueden encadenar", "Pasa el resultado de uno como entrada al siguiente"],
        ),
        Mission(
            num=5, title="Boss: Generator Expression",
            description="Usando una generator expression, calcula la suma de los cuadrados de los primeros 100 números naturales.\nResultado esperado: 338350",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="338350")],
            hints=["(x**2 for x in range(1, 101)) es una generator expression", "sum() suma todos los elementos"],
        ),
    ],
)
