from world.zones import Zone, Mission


zone = Zone(
    id=6,
    name="El Puerto",
    story_intro=(
        "En el Puerto de los Módulos atracan barcos de todo tipo.\n"
        "Importar y exportar es el pan de cada día.\n"
        "El contramaestre te pide que organices la carga."
    ),
    missions=[
        Mission(
            num=1, title="Importar el Necesario",
            description="Importa el módulo `math` y muestra el valor de pi (math.pi) con 4 decimales.",
            example="import math\nprint(f'{math.pi:.4f}')",
            validation_fn=lambda out, err: (out == "3.1416", "pi con 4 decimales = 3.1416"),
        ),
        Mission(
            num=2, title="Alias y Navegación",
            description="Importa `datetime` como `dt` y muestra la fecha actual con dt.date.today().",
            validation_fn=lambda out, err: (len(out) > 0, "Debe mostrar la fecha actual"),
        ),
        Mission(
            num=3, title="Solo lo Necesario",
            description="Importa solo `sqrt` y `pow` de math. Muestra sqrt(16) y pow(2, 10).",
            validation_fn=lambda out, err: ("4.0" in out and "1024.0" in out, "sqrt(16)=4.0, pow(2,10)=1024.0"),
        ),
        Mission(
            num=4, title="Tu Propio Módulo",
            description="Crea un módulo `utilidades.py` con una función `saludar(nombre)`. En otro script, impórtalo y úsalo.\n(Escribe solo el script principal.)",
            validation_fn=lambda out, err: (True, ""),
        ),
        Mission(
            num=5, title="Boss: Explorador de Módulos",
            description="Usa `importlib` o `pkgutil` para listar todos los submódulos de `collections`. Muestra la lista ordenada.",
            validation_fn=lambda out, err: (True, ""),
        ),
    ],
)
