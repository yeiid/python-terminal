from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=14,
    name="El Portal de Contexto",
    story_intro=(
        "Un portal dimensional se abre ante ti.\n"
        "Los contextos son pasajes entre mundos: entras, actúas, y al salir\n"
        "todo se limpia automáticamente. Domina el portal y cruza al otro lado."
    ),
    missions=[
        Mission(
            num=1, title="Abrir y Cerrar",
            description="Usa un context manager with open() para escribir 'Hola Mundo' en 'test.txt' y luego leerlo para mostrar su contenido.",
            execution_mode="script",
            code_template="with open('test.txt', 'w') as f:\n    f.write('Hola Mundo')\n\nwith open('test.txt', 'r') as f:\n    print(f.read())",
            test_cases=[TestCase(input="", expected="Hola Mundo")],
            hints=["with open() as f: maneja la apertura/cierre automático", "f.read() lee todo el contenido"],
        ),
        Mission(
            num=2, title="Context Manager Propio",
            description="Define una clase `Timer` que sea un context manager. Al entrar muestra 'Iniciando...' y al salir muestra 'Finalizado.'",
            execution_mode="script",
            code_template="class Timer:\n    def __enter__(self):\n        print('Iniciando...')\n        return self\n    def __exit__(self, *args):\n        print('Finalizado.')\n\nwith Timer():\n    pass",
            test_cases=[TestCase(input="", expected="Iniciando...\nFinalizado.")],
            hints=["__enter__ se ejecuta al entrar al with", "__exit__ se ejecuta al salir"],
        ),
        Mission(
            num=3, title="Contextlib",
            description="Usa @contextmanager de contextlib para crear un generador que muestre 'Entrando' antes del yield y 'Saliendo' después.",
            execution_mode="script",
            code_template="from contextlib import contextmanager\n\n@contextmanager\ndef mi_contexto():\n    print('Entrando')\n    yield\n    print('Saliendo')\n\nwith mi_contexto():\n    pass",
            test_cases=[TestCase(input="", expected="Entrando\nSaliendo")],
            hints=["@contextmanager decora un generador", "yield separa la entrada de la salida"],
        ),
        Mission(
            num=4, title="Manejando Excepciones en Contexto",
            description="Modifica el context manager Timer del ejercicio 2 para que capture excepciones y muestre 'Error capturado' sin propagarlo.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="Iniciando...\nError capturado\nFinalizado.")],
            hints=["__exit__ recibe (exc_type, exc_val, exc_tb)", "Retornar True suprime la excepción"],
        ),
        Mission(
            num=5, title="Boss: Pool de Conexiones",
            description="Crea un context manager `PoolConexiones` que mantenga un máximo de 2 conexiones.\nAl entrar, si hay menos de 2 conexiones activas, muestra 'Conexión asignada'.\nAl salir, muestra 'Conexión liberada'.\nSi ya hay 2 conexiones activas, muestra 'Pool lleno'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["Usa una variable de clase para contar conexiones activas", "__exit__ debe decrementar el contador"],
        ),
    ],
)
