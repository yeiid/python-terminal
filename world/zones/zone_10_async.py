from world.zones import Zone, Mission


zone = Zone(
    id=10,
    name="La Red",
    story_intro=(
        "La Red de la Concurrencia conecta toda la ciudad.\n"
        "Señales async viajan a la velocidad de la luz.\n"
        "La operadora te enseña a manejar múltiples canales."
    ),
    missions=[
        Mission(
            num=1, title="Async Primer",
            description="Define una función async `saludar()` que haga `await asyncio.sleep(0.1)` y luego print('Hola async!'). Ejecútala con asyncio.run().",
            example="import asyncio\n\nasync def saludar():\n    await asyncio.sleep(0.1)\n    print('Hola async!')\n\nasyncio.run(saludar())",
            validation_fn=lambda out, err: ('Hola async!' in out, 'Debe mostrar Hola async!'),
        ),
        Mission(
            num=2, title="Tareas Concurrentes",
            description="Crea dos tareas async que corran concurrentemente: `tarea1` que muestre 'A' tras 0.1s y `tarea2` que muestre 'B' tras 0.2s. Usa asyncio.gather().",
            validation_fn=lambda out, err: (out == "A\nB" or "A" in out, 'Debe mostrar A y B'),
        ),
        Mission(
            num=3, title="Timeout Control",
            description="Usa asyncio.wait_for() para ejecutar una tarea que tarda 5s pero con timeout de 1s. Captura la excepción y muestra 'Timeout'.",
            validation_fn=lambda out, err: ('Timeout' in out, 'Debe mostrar Timeout'),
        ),
        Mission(
            num=4, title="Produtor-Consumidor",
            description="Implementa un patrón productor-consumidor con asyncio.Queue. El productor pone 5 números, el consumidor los suma. Muestra el total.",
            validation_fn=lambda out, err: ('10' in out or '15' in out, 'Debe mostrar la suma'),
        ),
        Mission(
            num=5, title="Boss: Escáner de Puertos Async",
            description="Usando asyncio, escanea los puertos 80, 443, 8080 de 'localhost' o 'google.com'. Usa asyncio.open_connection con timeout. Muestra qué puertos están abiertos.",
            validation_fn=lambda out, err: (True, ''),
        ),
    ],
)
