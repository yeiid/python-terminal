from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=11,
    name="El Arsenal",
    story_intro=(
        "El Arsenal de Testing es donde el código se pone a prueba.\n"
        "Cada soldado verifica su equipo antes de la batalla.\n"
        "El instructor te exige que demuestres que tu código funciona."
    ),
    missions=[
        Mission(
            num=1, title="Assert Básico",
            description="Escribe una función `suma(a, b)` y prueba con assert que suma(2, 3) == 5. Si pasa, print('OK').",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="OK")],
            hints=["assert condición, mensaje verifica una condición", "Si la condición es True, no hace nada"],
        ),
        Mission(
            num=2, title="Test con unittest",
            description="Crea una clase `TestSuma(unittest.TestCase)` con un método `test_suma_positivos`. Ejecuta unittest.main().",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="OK")],
            hints=["class Test(unittest.TestCase): y métodos test_*", "unittest.main() ejecuta todos los tests"],
        ),
        Mission(
            num=3, title="Test de Excepciones",
            description="Escribe una función `dividir(a, b)` que levante ValueError si b==0. Prueba con assertRaises.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="OK")],
            hints=["with self.assertRaises(ValueError): espera una excepción", "La función debe lanzar ValueError"],
        ),
        Mission(
            num=4, title="SetUp y TearDown",
            description="Usa setUp para crear datos de prueba y tearDown para limpiar. Prueba una función que procese una lista.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="OK")],
            hints=["def setUp(self): se ejecuta antes de cada test", "def tearDown(self): se ejecuta después"],
        ),
        Mission(
            num=5, title="Boss: Test Parameterizado",
            description="Usando subTest o parametrización manual, prueba una función `es_par(n)` con varios casos: 2->True, 3->False, 0->True, -1->False.\n\nMuestra 'Todos los tests pasaron' si todo funciona, o el error si falla.",
            execution_mode="script",
            code_template="def es_par(n):\n    return n % 2 == 0\n\ncasos = [(2, True), (3, False), (0, True), (-1, False)]\ntodos_ok = True\nfor n, esperado in casos:\n    if es_par(n) != esperado:\n        print(f'ERROR: es_par({n}) != {esperado}')\n        todos_ok = False\n\nif todos_ok:\n    print('Todos los tests pasaron')",
            test_cases=[TestCase(input="", expected="Todos los tests pasaron")],
            hints=["Un bucle for recorre los casos", "assert condición o if para verificar"],
        ),
    ],
)
