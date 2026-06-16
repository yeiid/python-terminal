from world.zones import Zone, Mission


zone = Zone(
    id=3,
    name="La Fábrica",
    story_intro=(
        "La Fábrica de Funciones traquetea sin descanso.\n"
        "Cada engranaje es un def(), cada tubería un return.\n"
        "El capataz te exige que demuestres tu destreza."
    ),
    missions=[
        Mission(
            num=1, title="El Primer Engranaje",
            description="Define una función `suma(a, b)` que retorne a + b. Luego llama con suma(3, 4) y print del resultado.",
            example="def suma(a, b):\n    return a + b\nprint(suma(3, 4))",
            validation_fn=lambda out, err: (out == "7", "suma(3, 4) debe ser 7"),
        ),
        Mission(
            num=2, title="Argumentos Variables",
            description="Define `promedio(*args)` que retorne el promedio de todos los argumentos. Prueba con promedio(10, 20, 30).",
            validation_fn=lambda out, err: (out == "20.0", "promedio(10, 20, 30) = 20.0"),
        ),
        Mission(
            num=3, title="La Fábrica de Cierre",
            description="Define una función `multiplicador(n)` que retorne otra función que multiplique por n. Crea `por_dos = multiplicador(2)` y muestra `por_dos(5)`.",
            validation_fn=lambda out, err: (out == "10", "multiplicador(2)(5) = 10"),
        ),
        Mission(
            num=4, title="Documentación",
            description="Escribe una función `factorial(n)` con docstring que calcule el factorial recursivamente. Prueba con n=5.",
            validation_fn=lambda out, err: (out == "120", "factorial(5) = 120"),
        ),
        Mission(
            num=5, title="Boss: Calculadora Científica",
            description="Define funciones `raiz(n)`, `potencia(b, e)` y `seno(x)` (puedes usar math). Lee 3 números: operación, a, b. Si operación es 1: raiz(a); 2: potencia(a,b); 3: seno(a). Muestra el resultado con 3 decimales.",
            validation_fn=lambda out, err: (True, ""),
        ),
    ],
)
