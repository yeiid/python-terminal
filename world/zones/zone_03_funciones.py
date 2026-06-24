from world.zones import Zone, Mission, TestCase


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
            execution_mode="script",
            code_template="def suma(a, b):\n    return a + b\nprint(suma(3, 4))",
            test_cases=[TestCase(input="", expected="7")],
            hints=["def nombre(parametros): define una función", "return devuelve el resultado"],
        ),
        Mission(
            num=2, title="Argumentos Variables",
            description="Define `promedio(*args)` que retorne el promedio de todos los argumentos. Prueba con promedio(10, 20, 30).",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="20.0")],
            hints=["*args empaqueta argumentos en una tupla", "sum(args) / len(args) calcula el promedio"],
        ),
        Mission(
            num=3, title="La Fábrica de Cierre",
            description="Define una función `multiplicador(n)` que retorne otra función que multiplique por n. Crea `por_dos = multiplicador(2)` y muestra `por_dos(5)`.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="10")],
            hints=["Una función puede retornar otra función", "La función interna recuerda el valor de n"],
        ),
        Mission(
            num=4, title="Documentación",
            description="Escribe una función `factorial(n)` con docstring que calcule el factorial recursivamente. Prueba con n=5.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="120")],
            hints=["El docstring va entre triple comillas", "n! = n * (n-1)! con caso base n=1"],
        ),
        Mission(
            num=5, title="Boss: Calculadora Científica",
            description="Define funciones `raiz(n)`, `potencia(b, e)` y `seno(x)` (puedes usar math). Lee 3 números: operación, a, b. Si operación es 1: raiz(a); 2: potencia(a,b); 3: seno(a). Muestra el resultado con 3 decimales.",
            execution_mode="script",
            test_cases=[TestCase(input="1\n9\n0", expected="3.000")],
            hints=["import math para raiz y seno", "Usa match/case o if/elif para la operación"],
        ),
    ],
)
