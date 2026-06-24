from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=7,
    name="Los Archivos",
    story_intro=(
        "El Archivo Central guarda todos los secretos de la ciudad.\n"
        "Cada archivo es una puerta, cada directorio un pasillo.\n"
        "El bibliotecario te pide que organices los documentos."
    ),
    missions=[
        Mission(
            num=1, title="Escribir el Primer Documento",
            description="Escribe un programa que cree un archivo 'nota.txt' con el texto 'PyQuest rules!' y lo cierre.",
            execution_mode="script",
            code_template="with open('nota.txt', 'w') as f:\n    f.write('PyQuest rules!')\nprint('Archivo creado')",
            test_cases=[TestCase(input="", expected="Archivo creado")],
            hints=["with open('archivo', 'w') as f: para escribir", "Los archivos se cierran automáticamente con with"],
        ),
        Mission(
            num=2, title="Leer el Pasado",
            description="Lee el archivo 'nota.txt' que creaste y muestra su contenido.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="PyQuest rules!")],
            hints=["with open('nota.txt', 'r') as f: para leer", "f.read() devuelve todo el contenido"],
        ),
        Mission(
            num=3, title="Pathlib Explorer",
            description="Usa pathlib para crear la carpeta 'misiones/' y un archivo 'misiones/mision1.txt'. Luego lista los archivos en 'misiones/'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected=".txt")],
            hints=["from pathlib import Path", "Path('carpeta').mkdir() y Path('carpeta/archivo').touch()"],
        ),
        Mission(
            num=4, title="JSON Almacenado",
            description="Crea un dict {'nombre': 'PyQuest', 'version': 1} y guárdalo como 'config.json' con json.dump. Luego léelo y muestra la versión.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="1")],
            hints=["import json para serializar", "json.dump(dict, f) escribe y json.load(f) lee"],
        ),
        Mission(
            num=5, title="Boss: Analizador CSV",
            description=(
                "Crea un archivo CSV 'ventas.csv' con:\n"
                "producto,cantidad,precio\n"
                "manzanas,10,2.5\npanes,5,3.0\nleches,8,1.8\n"
                "Luego léelo y calcula el total de ingresos (cantidad*precio)."
            ),
            execution_mode="script",
            code_template="import csv\n\nwith open('ventas.csv', 'w', newline='') as f:\n    writer = csv.writer(f)\n    writer.writerow(['producto', 'cantidad', 'precio'])\n    writer.writerow(['manzanas', 10, 2.5])\n    writer.writerow(['panes', 5, 3.0])\n    writer.writerow(['leches', 8, 1.8])\n\ntotal = 0\nwith open('ventas.csv', 'r') as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        total += int(row['cantidad']) * float(row['precio'])\n\nprint(total)",
            test_cases=[TestCase(input="", expected="54.4")],
            hints=["import csv para archivos CSV", "Suma cantidad * precio de cada fila"],
        ),
    ],
)
