from world.zones import Zone, Mission


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
            example="print('Hola, PyQuest!')",
            validation_fn=lambda out, err: (out == "Hola, PyQuest!", "Debe mostrar 'Hola, PyQuest!'"),
        ),
        Mission(
            num=2, title="Variables del Destino",
            description="Crea una variable `nombre` con tu nombre y otra `edad` con un número. Luego muestra: 'Me llamo X y tengo Y años'",
            example='nombre = "Ana"\nedad = 25\nprint(f"Me llamo {nombre} y tengo {edad} años")',
            validation_fn=lambda out, err: (
                "Me llamo" in out and "y tengo" in out and "años" in out,
                "Formato: 'Me llamo X y tengo Y años'"
            ),
        ),
        Mission(
            num=3, title="Tipos y Tipo",
            description="Completa el código para que muestre el tipo de cada variable:\n\nx = 42\ny = 3.14\nz = 'hola'\nprint(type(x).__name__)\nprint(type(y).__name__)\nprint(type(z).__name__)",
            validation_fn=lambda out, err: (
                out == "int\nfloat\nstr",
                "Debe mostrar:\nint\nfloat\nstr"
            ),
        ),
        Mission(
            num=4, title="El Conversor",
            description="Escribe un programa que pida un número (input()), lo convierta a entero, lo multiplique por 2, y muestre el resultado.",
            example="num = int(input())\nprint(num * 2)",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=5, title="Boss: Calculadora de Propinas",
            description="Escribe un programa que lea dos números: total_cuenta y porcentaje_propina, y muestre:\n'Propina: $X. Total: $Y'\ncon 2 decimales.",
            example="total = float(input())\npct = float(input())\npropina = total * pct / 100\nprint(f'Propina: ${propina:.2f}. Total: ${total + propina:.2f}')",
            validation_fn=lambda out, err: (True, ""),
        ),
    ],
)
