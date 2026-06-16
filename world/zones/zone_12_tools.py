from world.zones import Zone, Mission


zone = Zone(
    id=12,
    name="El Cuartel",
    story_intro=(
        "El Cuartel General es el centro de operaciones.\n"
        "Aquí se manejan las herramientas del sistema.\n"
        "El comandante te asigna misiones del mundo real."
    ),
    missions=[
        Mission(
            num=1, title="OS Explorer",
            description="Usa el módulo os para mostrar el directorio actual (getcwd()) y listar los archivos (listdir('.')).",
            validation_fn=lambda out, err: (len(out) > 0, 'Debe mostrar el directorio actual y archivos'),
        ),
        Mission(
            num=2, title="Argumentos de Línea",
            description="Usa argparse para crear un programa que acepte --nombre y --edad y muestre 'Hola NOMBRE, tienes EDAD años'.",
            validation_fn=lambda out, err: (True, ''),
        ),
        Mission(
            num=3, title="Subprocess Power",
            description="Usa subprocess.run() para ejecutar 'echo Hola desde subprocess' y captura/muestra la salida.",
            validation_fn=lambda out, err: ('Hola desde subprocess' in out, 'Debe capturar la salida del comando'),
        ),
        Mission(
            num=4, title="Solicitud HTTP",
            description="Usa urllib.request o requests (si está instalado) para hacer GET a 'https://httpbin.org/get' y mostrar el status code.",
            validation_fn=lambda out, err: ('200' in out, 'Status code debe ser 200'),
        ),
        Mission(
            num=5, title="Boss: CLI Definitiva",
            description=(
                "Crea una CLI completa con argparse que:\n"
                "- Acepte un comando: 'suma', 'multiplica', 'archivo'\n"
                "- Para suma: --a --b (enteros)\n"
                "- Para multiplica: --a --b (enteros)\n"
                "- Para archivo: --ruta (lee y muestra el archivo)\n"
                "Prueba con suma 5 7."
            ),
            validation_fn=lambda out, err: (True, ''),
        ),
    ],
)
