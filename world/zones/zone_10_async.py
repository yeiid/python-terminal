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
            num=5, title="Boss: Descargador Concurrente",
            description="Usando asyncio, crea una función `fetch_url(url, delay)` que espere `delay` segundos y luego devuelva `f'Descargado: {url}'`. Usa asyncio.gather para descargar 3 URLs en paralelo. Muestra los resultados ordenados.",
            execution_mode="script",
            code_template="import asyncio\n\nasync def fetch_url(url, delay):\n    await asyncio.sleep(delay)\n    return f'Descargado: {url}'\n\nasync def main():\n    tareas = [\n        fetch_url('https://ejemplo.com/1', 0.3),\n        fetch_url('https://ejemplo.com/2', 0.1),\n        fetch_url('https://ejemplo.com/3', 0.2),\n    ]\n    resultados = await asyncio.gather(*tareas)\n    for r in resultados:\n        print(r)\n\nasyncio.run(main())",
            test_cases=[TestCase(input="", expected="Descargado: https://ejemplo.com/1\nDescargado: https://ejemplo.com/2\nDescargado: https://ejemplo.com/3")],
            hints=["asyncio.gather() ejecuta múltiples corrutinas en paralelo", "Usa await asyncio.sleep() para simular latencia"],
        ),
    ],
)
