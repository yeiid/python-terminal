from world.zones import Zone, Mission, TestCase


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
            execution_mode="script",
            code_template="import asyncio\n\nasync def saludar():\n    await asyncio.sleep(0.1)\n    print('Hola async!')\n\nasyncio.run(saludar())",
            test_cases=[TestCase(input="", expected="Hola async!")],
            hints=["async def define una corrutina", "await espera una operación asíncrona"],
        ),
        Mission(
            num=2, title="Tareas Concurrentes",
            description="Crea dos tareas async que corran concurrentemente: `tarea1` que muestre 'A' tras 0.1s y `tarea2` que muestre 'B' tras 0.2s. Usa asyncio.gather().",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="A\nB")],
            hints=["asyncio.gather() ejecuta múltiples tareas", "asyncio.sleep() simula una operación lenta"],
        ),
        Mission(
            num=3, title="Timeout Control",
            description="Usa asyncio.wait_for() para ejecutar una tarea que tarda 5s pero con timeout de 1s. Captura la excepción y muestra 'Timeout'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="Timeout")],
            hints=["asyncio.wait_for() añade un límite de tiempo", "Captura asyncio.TimeoutError"],
        ),
        Mission(
            num=4, title="Produtor-Consumidor",
            description="Implementa un patrón productor-consumidor con asyncio.Queue. El productor pone 5 números, el consumidor los suma. Muestra el total.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="10")],
            hints=["asyncio.Queue() para comunicación entre tareas", "await queue.put() y await queue.get()"],
        ),
        Mission(
            num=5, title="Boss: Escáner de Puertos Async",
            description="Usando asyncio, escanea los puertos 80, 443, 8080 de 'localhost' o 'google.com'. Usa asyncio.open_connection con timeout. Muestra qué puertos están abiertos.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["asyncio.open_connection(host, puerto) abre conexión", "Usa asyncio.wait_for con timeout"],
        ),
    ],
)
