from world.zones import Zone, Mission


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
            example="with open('nota.txt', 'w') as f:\n    f.write('PyQuest rules!')\nprint('Archivo creado')",
            validation_fn=lambda out, err: ('Archivo creado' in out, 'Debe mostrar confirmación'),
        ),
        Mission(
            num=2, title="Leer el Pasado",
            description="Lee el archivo 'nota.txt' que creaste y muestra su contenido.",
            validation_fn=lambda out, err: ('PyQuest rules!' in out, 'Debe mostrar el contenido del archivo'),
        ),
        Mission(
            num=3, title="Pathlib Explorer",
            description="Usa pathlib para crear la carpeta 'misiones/' y un archivo 'misiones/mision1.txt'. Luego lista los archivos en 'misiones/'.",
            validation_fn=lambda out, err: ('.txt' in out, 'Debe listar archivos .txt'),
        ),
        Mission(
            num=4, title="JSON Almacenado",
            description="Crea un dict {'nombre': 'PyQuest', 'version': 1} y guárdalo como 'config.json' con json.dump. Luego léelo y muestra la versión.",
            validation_fn=lambda out, err: ('1' in out, 'Versión debe ser 1'),
        ),
        Mission(
            num=5, title="Boss: Analizador CSV",
            description=(
                "Crea un archivo CSV 'ventas.csv' con:\n"
                "producto,cantidad,precio\n"
                "manzanas,10,2.5\npanes,5,3.0\nleches,8,1.8\n"
                "Luego léelo y calcula el total de ingresos (cantidad*precio)."
            ),
            validation_fn=lambda out, err: (True, ''),
        ),
    ],
)
