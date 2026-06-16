from world.zones import Zone, Mission, TestCase


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
            execution_mode="script",
            test_cases=[TestCase(input="", expected="anillo")],
            hints=["list.append() agrega al final", "print(lista) muestra el contenido"],
        ),
        Mission(
            num=2, title="El Dict del Mercader",
            description="Crea un dict: {'nombre': 'Mercader', 'items': 15, 'oro': 200}. Muestra sus keys.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="nombre")],
            hints=["dict.keys() devuelve las claves", "Las claves van separadas por comas"],
        ),
        Mission(
            num=3, title="Conjuntos Únicos",
            description="Dadas listas a = [1, 2, 3, 3, 4] y b = [3, 4, 5, 6], muestra los elementos comunes (intersección).",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="3, 4")],
            hints=["set(a) & set(b) da la intersección", "Los sets eliminan duplicados automáticamente"],
        ),
        Mission(
            num=4, title="Tuple Packing",
            description="Crea una tuple `coord = (10, 20)` y desempaqueta en x, y. Muestra 'x=10, y=20'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="x=10, y=20")],
            hints=["x, y = coord desempaqueta la tupla", "Usa print(f'...') para formatear"],
        ),
        Mission(
            num=5, title="Boss: Analizador de Ventas",
            description="Dado un dict de ventas: {'lunes': 120, 'martes': 85, 'miercoles': 200, 'jueves': 95, 'viernes': 150}, calcula y muestra: total, promedio, día con más ventas.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="650")],
            hints=["sum(dict.values()) suma todos los valores", "max(dict, key=dict.get) da la clave con mayor valor"],
        ),
    ],
)
