from world.zones import Zone, Mission


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
            validation_fn=lambda out, err: ('OK' in out, 'Debe mostrar OK'),
        ),
        Mission(
            num=2, title="Test con unittest",
            description="Crea una clase `TestSuma(unittest.TestCase)` con un método `test_suma_positivos`. Ejecuta unittest.main().",
            validation_fn=lambda out, err: ('OK' in out or 'ok' in out, 'Tests deben pasar'),
        ),
        Mission(
            num=3, title="Test de Excepciones",
            description="Escribe una función `dividir(a, b)` que levante ValueError si b==0. Prueba con assertRaises.",
            validation_fn=lambda out, err: ('OK' in out or 'ok' in out, 'Test de excepción debe pasar'),
        ),
        Mission(
            num=4, title="SetUp y TearDown",
            description="Usa setUp para crear datos de prueba y tearDown para limpiar. Prueba una función que procese una lista.",
            validation_fn=lambda out, err: ('OK' in out or 'ok' in out, 'Tests deben pasar'),
        ),
        Mission(
            num=5, title="Boss: Test Parameterizado",
            description="Usando subTest o parametrización manual, prueba una función `es_par(n)` con varios casos: 2->True, 3->False, 0->True, -1->False.",
            validation_fn=lambda out, err: (True, ''),
        ),
    ],
)
