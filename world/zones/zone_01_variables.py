from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=1,
    name="Barrio Base",
    story_intro=(
        "Llegas a las afueras de PyQuest City. Un cartel parpadea:\n"
        "«Todo gran dev empieza con un print().»\n"
        "Una terminal oxidada te pide que demuestres lo básico."
    ),
    missions=[
        Mission(
            num=1, title="El Primer Saludo",
            description="Escribe un print() que muestre 'Hola, PyQuest!'",
            execution_mode="script",
            code_template="print('Hola, PyQuest!')",
            test_cases=[TestCase(input="", expected="Hola, PyQuest!")],
            hints=["Usa print() para mostrar texto", "El mensaje debe ser exactamente 'Hola, PyQuest!'"],
        ),
        Mission(
            num=2, title="Variables del Destino",
            description="Crea una variable `nombre` con tu nombre y otra `edad` con un número. Luego muestra: 'Me llamo X y tengo Y años'",
            execution_mode="script",
            code_template='nombre = "Ana"\nedad = 25\nprint(f"Me llamo {nombre} y tengo {edad} años")',
            test_cases=[TestCase(input="", expected="Me llamo")],
            hints=["Usa f-strings para formatear", "Las variables se insertan con {llaves}"],
        ),
        Mission(
            num=3, title="Tipos y Tipo",
            description="Completa el código para que muestre el tipo de cada variable:\n\nx = 42\ny = 3.14\nz = 'hola'\nprint(type(x).__name__)\nprint(type(y).__name__)\nprint(type(z).__name__)",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="int\nfloat\nstr")],
            hints=["type() devuelve el tipo de un objeto", "__name__ da el nombre del tipo como string"],
        ),
        Mission(
            num=4, title="El Conversor",
            description="Escribe un programa que pida un número (input()), lo convierta a entero, lo multiplique por 2, y muestre el resultado.",
            execution_mode="script",
            code_template="num = int(input())\nprint(num * 2)",
            test_cases=[TestCase(input="", expected="")],
            hints=["int() convierte string a entero", "input() siempre devuelve un string"],
        ),
        Mission(
            num=5, title="Boss: Calculadora de Propinas",
            description="Escribe un programa que lea dos números: total_cuenta y porcentaje_propina, y muestre:\n'Propina: $X. Total: $Y'\ncon 2 decimales.",
            execution_mode="script",
            code_template="total = float(input())\npct = float(input())\npropina = total * pct / 100\nprint(f'Propina: ${propina:.2f}. Total: ${total + propina:.2f}')",
            test_cases=[TestCase(input="", expected="")],
            hints=["Usa float() para números decimales", "Formatea con :.2f para 2 decimales"],
        ),
    ],
)
