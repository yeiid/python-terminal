from world.zones import Zone, Mission


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
            example="x = 10\nif x % 2 == 0:\n    print('Par')\nelse:\n    print('Impar')",
            validation_fn=lambda out, err: (out == "Par", "x=10 debe mostrar 'Par'"),
        ),
        Mission(
            num=2, title="El Bucle Infinito",
            description="Usa un for para mostrar los números del 1 al 5, uno por línea.",
            example="for i in range(1, 6):\n    print(i)",
            validation_fn=lambda out, err: (out == "1\n2\n3\n4\n5", "Debe mostrar 1 al 5 en líneas separadas"),
        ),
        Mission(
            num=3, title="Comprehension Park",
            description="Usando list comprehension, genera [0, 2, 4, 6, 8] y muéstralo.",
            validation_fn=lambda out, err: (
                out.strip("[]") == "0, 2, 4, 6, 8" or out == "[0, 2, 4, 6, 8]",
                "Debe generar [0, 2, 4, 6, 8]"
            ),
        ),
        Mission(
            num=4, title="El Filtro",
            description="Dada la lista nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], muestra solo los pares usando filter o comprehension.",
            validation_fn=lambda out, err: (out == "2\n4\n6\n8\n10" or "[2, 4, 6, 8, 10]" in out, "Filtrar pares de 1 a 10"),
        ),
        Mission(
            num=5, title="Boss: FizzBuzz",
            description="Escribe un programa que muestre del 1 al 20, pero:\n- Múltiplos de 3 → 'Fizz'\n- Múltiplos de 5 → 'Buzz'\n- Ambos → 'FizzBuzz'",
            validation_fn=lambda out, err: (
                "Fizz" in out and "Buzz" in out and "FizzBuzz" in out,
                "Debe contener Fizz, Buzz y FizzBuzz"
            ),
        ),
    ],
)
