from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=13,
    name="El Abismo de Excepciones",
    story_intro=(
        "Has caído al Abismo, donde el código se rompe intencionadamente.\n"
        "Aquí, las excepciones son la norma y quien las domina sobrevive.\n"
        "Aprende a lanzar, capturar y encadenar errores."
    ),
    missions=[
        Mission(
            num=1, title="Captura el Error",
            description="Escribe un programa que intente convertir 'abc' a int con int(), capture ValueError y muestre 'Error de tipo'.",
            execution_mode="script",
            code_template="try:\n    int('abc')\nexcept ValueError:\n    print('Error de tipo')",
            test_cases=[TestCase(input="", expected="Error de tipo")],
            hints=["Usa try/except para capturar la excepción", "ValueError es el tipo de error al convertir"],
        ),
        Mission(
            num=2, title="Múltiples Excepciones",
            description="Escribe código que intente x = 1/0, capture ZeroDivisionError y también KeyboardInterrupt, mostrando 'Error matemático' o 'Interrupción'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="Error matemático")],
            hints=["Pon 1/0 dentro del try", "Usa except (Tipo1, Tipo2) para múltiples excepciones"],
        ),
        Mission(
            num=3, title="Finally Siempre",
            description="Escribe un programa que intente abrir un archivo 'data.txt', capture FileNotFoundError mostrando 'No existe', y en finally muestre 'Cerrando recursos'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="No existe\nCerrando recursos")],
            hints=["finally se ejecuta siempre, haya o no error", "open('data.txt') lanza FileNotFoundError si no existe"],
        ),
        Mission(
            num=4, title="Lanzar Propia Excepción",
            description="Define una función `validar_edad(n)` que lance ValueError('Edad inválida') si n < 0 o n > 150, y retorne 'Ok' si es válida. Llámala con 200 y captura el error.",
            execution_mode="script",
            code_template="def validar_edad(n):\n    if n < 0 or n > 150:\n        raise ValueError('Edad inválida')\n    return 'Ok'\n\ntry:\n    print(validar_edad(200))\nexcept ValueError as e:\n    print(e)",
            test_cases=[TestCase(input="", expected="Edad inválida")],
            hints=["raise ValueError('mensaje') lanza una excepción", "Captúrala con except ValueError as e"],
        ),
        Mission(
            num=5, title="Boss: Calculadora Robusta",
            description="Escribe una calculadora que lea dos números y un operador (+, -, *, /).\nManeja: ValueError si los números no son válidos, ZeroDivisionError si se divide por 0, y TypeError si el operador no es reconocido.\nMuestra resultados o mensajes de error apropiados.",
            execution_mode="script",
            test_cases=[
                TestCase(input="10\n0\n/", expected="Error: división por cero"),
            ],
            hints=["Usa try/except alrededor de la conversión a float", "ZeroDivisionError ocurre con float('inf') al dividir por 0"],
        ),
    ],
)
