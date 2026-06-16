from world.zones import Zone, Mission


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
            validation_fn=lambda out, err: ("1" in out and "5" in out, "Debe contar del 1 al 5"),
        ),
        Mission(
            num=2, title="Yield From",
            description="Usa `yield from` para aplanar una lista de listas: [[1,2], [3,4], [5,6]] y mostrar los elementos.",
            validation_fn=lambda out, err: (out == "1\n2\n3\n4\n5\n6" or "1, 2, 3, 4, 5, 6" in out, "Aplanar lista anidada"),
        ),
        Mission(
            num=3, title="Infinito Controlado",
            description="Crea un generator `pares()` que genere números pares infinitamente. Toma los primeros 10 con un bucle y break.",
            validation_fn=lambda out, err: (out == "0\n2\n4\n6\n8\n10\n12\n14\n16\n18", "Primeros 10 pares (0-18)"),
        ),
        Mission(
            num=4, title="Pipeline Generator",
            description="Crea dos generators: `cuadrados(nums)` que eleve al cuadrado, y `mostrar(nums)` que imprima. Conéctalos en pipeline: range(1, 6) -> cuadrados -> mostrar.",
            validation_fn=lambda out, err: (out == "1\n4\n9\n16\n25", "Cuadrados de 1 a 5"),
        ),
        Mission(
            num=5, title="Boss: Generator Expression",
            description="Usando una generator expression, calcula la suma de los cuadrados de los primeros 100 números naturales.\nResultado esperado: 338350",
            validation_fn=lambda out, err: ("338350" in out, "Suma cuadrados 1..100 = 338350"),
        ),
    ],
)
