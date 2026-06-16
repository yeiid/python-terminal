from world.zones import Zone, Mission


zone = Zone(
    id=4,
    name="El Mercado",
    story_intro=(
        "El Mercado de Estructuras bulle de actividad.\n"
        "Puestos de listas, carretas de dicts, jaulas de sets.\n"
        "El vendedor te reta a organizar sus datos."
    ),
    missions=[
        Mission(
            num=1, title="Inventario en Lista",
            description="Crea una lista con: 'espada', 'escudo', 'pocion'. Agrega 'anillo' al final. Muestra la lista.",
            validation_fn=lambda out, err: (
                "'espada'" in out and "'anillo'" in out,
                "Lista debe contener espada, escudo, pocion, anillo"
            ),
        ),
        Mission(
            num=2, title="El Dict del Mercader",
            description="Crea un dict: {'nombre': 'Mercader', 'items': 15, 'oro': 200}. Muestra sus keys.",
            validation_fn=lambda out, err: (
                "nombre" in out and "items" in out and "oro" in out,
                "Keys: nombre, items, oro"
            ),
        ),
        Mission(
            num=3, title="Conjuntos Únicos",
            description="Dadas listas a = [1, 2, 3, 3, 4] y b = [3, 4, 5, 6], muestra los elementos comunes (intersección).",
            validation_fn=lambda out, err: (
                "3" in out and "4" in out,
                "Intersección de [1,2,3,3,4] y [3,4,5,6] = {3, 4}"
            ),
        ),
        Mission(
            num=4, title="Tuple Packing",
            description="Crea una tuple `coord = (10, 20)` y desempaqueta en x, y. Muestra 'x=10, y=20'.",
            validation_fn=lambda out, err: (out == "x=10, y=20", "Formato: 'x=10, y=20'"),
        ),
        Mission(
            num=5, title="Boss: Analizador de Ventas",
            description="Dado un dict de ventas: {'lunes': 120, 'martes': 85, 'miercoles': 200, 'jueves': 95, 'viernes': 150}, calcula y muestra: total, promedio, día con más ventas.",
            validation_fn=lambda out, err: (
                "650" in out and "miercoles" in out,
                "Total=650, Mejor día=miercoles"
            ),
        ),
    ],
)
