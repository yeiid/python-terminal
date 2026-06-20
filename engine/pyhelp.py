"""PyQuest Interactive Python Documentation — Aprende Python con ejemplos interactivos.

Uso desde el juego:
  /docs           → Abre el navegador de documentación
  /docs <tema>    → Va directo a un tema
  /docs buscar <q>→ Busca en la documentación

Cada tema incluye:
  - Explicación clara
  - Ejemplos de código que puedes ejecutar
  - Ejercicios prácticos
"""

import textwrap
from dataclasses import dataclass, field
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align
from rich.columns import Columns
from engine.console import console
from engine.executor import execute_code
from engine.curriculum import (
    mark_viewed, mark_example_run, get_topic_progress,
    STATUS_ICONS, STATUS_LABELS,
)


@dataclass
class PyExample:
    title: str
    code: str
    output: str = ""
    description: str = ""


@dataclass
class PyTopic:
    id: str
    title: str
    category: str
    icon: str
    level: str  # Principiante, Intermedio, Avanzado
    summary: str
    content: str
    examples: list[PyExample] = field(default_factory=list)
    related: list[str] = field(default_factory=list)


TOPICS: list[PyTopic] = [
    # ─── NIVEL 1: Principiante ───
    PyTopic(
        id="variables",
        title="Variables y Tipos de Datos",
        category="Fundamentos",
        icon="📦",
        level="Principiante",
        summary="Cómo guardar información en variables y los tipos básicos de Python.",
        content=textwrap.dedent("""\
            [bold]Variables[/] son contenedores para guardar datos.
            Python es de [bold]tipado dinámico[/] — no necesitas declarar el tipo.

            [bold]Tipos básicos:[/]
              • [cyan]int[/]    → Números enteros (1, 42, -7)
              • [cyan]float[/]  → Números decimales (3.14, -0.5)
              • [cyan]str[/]    → Texto ("Hola", 'Python')
              • [cyan]bool[/]   → True / False
              • [cyan]None[/]   → Ausencia de valor

            [bold]Buenas prácticas:[/]
              • Usa nombres descriptivos: [green]edad[/] en vez de [red]e[/]
              • Usa snake_case: [green]mi_variable[/]
              • Las constantes se escriben en MAYÚSCULAS: [green]PI = 3.1416[/]
        """),
        examples=[
            PyExample(
                title="Variables básicas",
                code="nombre = \"Ana\"\nedad = 25\naltura = 1.68\nes_estudiante = True\n\nprint(f\"{nombre} tiene {edad} años y mide {altura}m\")\nprint(\"¿Es estudiante?\", es_estudiante)",
                description="Declara variables de distintos tipos y las usa.",
            ),
            PyExample(
                title="Tipos dinámicos",
                code="x = 42\nprint(type(x))  # int\n\nx = \"ahora soy texto\"\nprint(type(x))  # str\n\nx = 3.14\nprint(type(x))  # float",
                description="Python permite reasignar una variable a otro tipo.",
            ),
            PyExample(
                title="Conversión entre tipos",
                code='numero = "42"\nprint(type(numero))\n\nconvertido = int(numero)\nprint(convertido + 8)  # 50\n\nprint("La respuesta es " + str(42))',
                description="Usa int(), str(), float() para convertir entre tipos.",
            ),
        ],
        related=["strings", "operadores"],
    ),
    PyTopic(
        id="strings",
        title="Strings (Cadenas de Texto)",
        category="Fundamentos",
        icon="📝",
        level="Principiante",
        summary="Trabaja con texto: métodos, formato y manipulación.",
        content=textwrap.dedent("""\
            Los [bold]strings[/] son texto. Se escriben con [cyan]''[/] o [cyan]""[/].

            [bold]Características:[/]
              • [cyan]len()[/]       → Longitud del string
              • [cyan].upper()[/]    → Mayúsculas
              • [cyan].lower()[/]    → Minúsculas
              • [cyan].split()[/]    → Divide en lista
              • [cyan].join()[/]     → Une una lista
              • [cyan].strip()[/]    → Quita espacios al inicio/final
              • [cyan].replace()[/]  → Reemplaza texto

            [bold]Formato:[/]
              • f-strings: [green]f"Hola, {nombre}"[/]
              • .format(): [green]"Hola, {}".format(nombre)[/]
              • %-format:  [green]"Hola, %s" % nombre[/]
        """),
        examples=[
            PyExample(
                title="Métodos de string",
                code='texto = "  hola Python  "\nprint(texto.strip())\nprint(texto.upper())\nprint(texto.replace("Python", "Mundo"))\nprint(texto.split())',
                description="Los strings tienen muchos métodos útiles.",
            ),
            PyExample(
                title="f-strings",
                code="nombre = \"Carlos\"\nlenguaje = \"Python\"\nedad = 30\n\nmensaje = f\"{nombre} programa en {lenguaje} desde hace {edad} años\"\nprint(mensaje)",
                description="f-strings son la forma más moderna de formatear texto.",
            ),
            PyExample(
                title="Rebanado (slicing)",
                code='texto = "Python"\nprint(texto[0])     # P\nprint(texto[-1])    # n\nprint(texto[0:3])   # Pyt\nprint(texto[::2])   # Pto\nprint(texto[::-1])  # nohtyP (invertido)',
                description="Accede a partes de un string con slicing [inicio:fin:paso].",
            ),
        ],
        related=["variables", "listas"],
    ),
    PyTopic(
        id="listas",
        title="Listas",
        category="Estructuras de Datos",
        icon="📋",
        level="Principiante",
        summary="Colecciones ordenadas y mutables de elementos.",
        content=textwrap.dedent("""\
            Las [bold]listas[/] guardan múltiples valores en orden.
            Se crean con [cyan][][/] y pueden contener cualquier tipo.

            [bold]Operaciones principales:[/]
              • [cyan].append()[/]   → Agrega al final
              • [cyan].insert()[/]   → Inserta en posición
              • [cyan].remove()[/]   → Quita por valor
              • [cyan].pop()[/]      → Quita y retorna el último
              • [cyan].sort()[/]     → Ordena
              • [cyan].reverse()[/]  → Invierte
              • [cyan]len()[/]       → Número de elementos
              • [cyan]in[/]          → Verifica si existe

            [bold]Comprensión de listas:[/]
              [green][x**2 for x in range(10) if x % 2 == 0][/]
              → [0, 4, 16, 36, 64]
        """),
        examples=[
            PyExample(
                title="Operaciones básicas",
                code="frutas = ['manzana', 'banana', 'cereza']\nfrutas.append('dátil')\nfrutas.insert(1, 'arándano')\nfrutas.remove('banana')\nprint(frutas)\nprint(f\"Tengo {len(frutas)} frutas\")",
                description="Agregar, insertar y eliminar elementos.",
            ),
            PyExample(
                title="List Comprehension",
                code="numeros = [1, 2, 3, 4, 5, 6]\npares = [n for n in numeros if n % 2 == 0]\ncuadrados = [n**2 for n in numeros]\n\nprint(f\"Original: {numeros}\")\nprint(f\"Pares: {pares}\")\nprint(f\"Cuadrados: {cuadrados}\")",
                description="Crea nuevas listas a partir de existentes en una línea.",
            ),
            PyExample(
                title="Iterar una lista",
                code='colores = ["rojo", "verde", "azul"]\nfor color in colores:\n    print(f"  🎨 {color}")\n\nfor i, color in enumerate(colores, 1):\n    print(f"{i}. {color}")',
                description="Recorre listas con for y enumerate.",
            ),
        ],
        related=["strings", "dicts", "bucles"],
    ),
    PyTopic(
        id="condicionales",
        title="Condicionales: if/elif/else",
        category="Fundamentos",
        icon="🔀",
        level="Principiante",
        summary="Toma decisiones en tu código con if, elif y else.",
        content=textwrap.dedent("""\
            Las [bold]condicionales[/] ejecutan código según condiciones.

            [bold]Estructura:[/]
              [green]if[/] condición:
                  [dim]# código si True[/]
              [green]elif[/] otra_condición:
                  [dim]# código si la primera es False y esta True[/]
              [green]else[/]:
                  [dim]# código si todas son False[/]

            [bold]Operadores de comparación:[/]
              [cyan]==[/]  igual  |  [cyan]!=[/]  distinto
              [cyan]>[/]   mayor  |  [cyan]<[/]   menor
              [cyan]>=[/]  mayor igual  |  [cyan]<=[/]  menor igual

            [bold]Operadores lógicos:[/]
              [cyan]and[/] — ambas condiciones True
              [cyan]or[/]  — al menos una True
              [cyan]not[/] — invierte el valor
        """),
        examples=[
            PyExample(
                title="Condicional básica",
                code="edad = 18\n\nif edad >= 18:\n    print(\"Eres mayor de edad\")\nelse:\n    print(\"Eres menor de edad\")",
                description="Estructura if/else simple.",
            ),
            PyExample(
                title="Múltiples condiciones",
                code="nota = 85\n\nif nota >= 90:\n    print(\"Excelente\")\nelif nota >= 70:\n    print(\"Bien\")\nelif nota >= 50:\n    print(\"Suficiente\")\nelse:\n    print(\"Necesitas mejorar\")",
                description="Encadena condiciones con elif.",
            ),
            PyExample(
                title="Operadores lógicos",
                code="edad = 25\ntiene_licencia = True\n\nif edad >= 18 and tiene_licencia:\n    print(\"Puedes conducir\")\nelif edad >= 18 and not tiene_licencia:\n    print(\"Saca tu licencia primero\")\nelse:\n    print(\"Eres muy joven para conducir\")",
                description="Combina condiciones con and, or, not.",
            ),
        ],
        related=["variables", "bucles", "operadores"],
    ),
    PyTopic(
        id="bucles",
        title="Bucles: for y while",
        category="Fundamentos",
        icon="🔄",
        level="Principiante",
        summary="Repite código con for (colecciones) y while (condiciones).",
        content=textwrap.dedent("""\
            Los [bold]bucles[/] repiten código múltiples veces.

            [bold]for[/] — Itera sobre una secuencia:
              [green]for[/] elemento [green]in[/] colección:
                  [dim]# código por cada elemento[/]

            [bold]while[/] — Repite mientras condición sea True:
              [green]while[/] condición:
                  [dim]# código mientras condición sea True[/]

            [bold]Control de bucles:[/]
              • [cyan]break[/]    → Sale del bucle
              • [cyan]continue[/] → Salta a la siguiente iteración
              • [cyan]else[/]     → Se ejecuta si no hubo break
        """),
        examples=[
            PyExample(
                title="Bucle for básico",
                code="for i in range(5):\n    print(f\"Iteración {i}\")",
                description="range(5) genera 0, 1, 2, 3, 4.",
            ),
            PyExample(
                title="Recorrer una lista",
                code='lenguajes = ["Python", "Java", "JavaScript", "Go"]\nfor lang in lenguajes:\n    if lang == "Python":\n        print(f"{lang} 🐍 — ¡El mejor!")\n    else:\n        print(lang)',
                description="Itera sobre los elementos de una lista.",
            ),
            PyExample(
                title="while con break",
                code="contador = 0\nwhile True:\n    contador += 1\n    print(f\"Intento {contador}\")\n    if contador >= 3:\n        print(\"¡Listo!\")\n        break",
                description="while True con break para salir controladamente.",
            ),
        ],
        related=["listas", "condicionales", "range"],
    ),
    # ─── NIVEL 2: Intermedio ───
    PyTopic(
        id="funciones",
        title="Funciones",
        category="Fundamentos",
        icon="⚙️",
        level="Intermedio",
        summary="Define bloques de código reutilizables con def.",
        content=textwrap.dedent("""\
            Las [bold]funciones[/] son bloques de código reutilizables.

            [green]def[/] nombre_funcion(param1, param2):
                [dim]# cuerpo de la función[/]
                [green]return[/] resultado

            [bold]Conceptos clave:[/]
              • [cyan]return[/] — retorna un valor (None si no se usa)
              • [cyan]args[/]   — argumentos posicionales
              • [cyan]kwargs[/]  — argumentos con nombre (palabra_clave=valor)
              • [cyan]*args[/]  — número variable de args posicionales
              • [cyan]**kwargs[/] — número variable de kwargs
              • [cyan]lambda[/] — función anónima de una línea
        """),
        examples=[
            PyExample(
                title="Función básica",
                code="def saludar(nombre):\n    return f\"¡Hola, {nombre}!\"\n\nprint(saludar(\"Mundo\"))\n\n# También se puede asignar a variable\nsaludo = saludar(\"Python\")\nprint(saludo)",
                description="Define y llama una función simple.",
            ),
            PyExample(
                title="Args y kwargs",
                code="def presentar(nombre, *hobbies, **datos):\n    print(f\"{nombre} tiene {len(hobbies)} hobbies\")\n    print(f\"Hobbies: {', '.join(hobbies)}\")\n    for clave, valor in datos.items():\n        print(f\"  {clave}: {valor}\")\n\npresentar(\"Ana\", \"leer\", \"correr\", edad=28, ciudad=\"Madrid\")",
                description="Usa *args y **kwargs para argumentos flexibles.",
            ),
            PyExample(
                title="Lambda (función anónima)",
                code="numeros = [1, 2, 3, 4, 5]\n\n# Función lambda que duplica\ndupli = list(map(lambda x: x * 2, numeros))\nprint(f\"Duplicados: {dupli}\")\n\n# Ordenar por criterio\npersonas = [(\"Ana\", 25), (\"Luis\", 18), (\"Carlos\", 30)]\nordenadas = sorted(personas, key=lambda p: p[1])\nprint(f\"Por edad: {ordenadas}\")",
                description="Lambda es una función de una línea sin nombre.",
            ),
        ],
        related=["variables", "listas", "modulos"],
    ),
    PyTopic(
        id="dicts",
        title="Diccionarios",
        category="Estructuras de Datos",
        icon="📖",
        level="Intermedio",
        summary="Colecciones clave-valor para datos estructurados.",
        content=textwrap.dedent("""\
            Los [bold]diccionarios[/] guardan pares clave:valor.
            Se crean con [cyan]{}[/] o [cyan]dict()[/].

            [bold]Operaciones:[/]
              • [cyan]dict[clave][/]     → Acceder (KeyError si no existe)
              • [cyan]dict.get(clave)[/] → Acceder (None si no existe)
              • [cyan]dict[clave] = val[/]→ Asignar/actualizar
              • [cyan].keys()[/]    → Todas las claves
              • [cyan].values()[/]  → Todos los valores
              • [cyan].items()[/]   → Pares (clave, valor)
              • [cyan].update()[/]  → Fusionar otro dict
        """),
        examples=[
            PyExample(
                title="Crear y acceder",
                code='persona = {\n    "nombre": "Ana",\n    "edad": 28,\n    "lenguajes": ["Python", "Go"]\n}\n\nprint(persona["nombre"])\nprint(persona.get("edad"))\nprint(persona.get("pais", "No especificado"))\n\npersona["edad"] = 29\nprint(persona)',
                description="Los diccionarios almacenan datos con nombre.",
            ),
            PyExample(
                title="Recorrer un dict",
                code='capitales = {\n    "Perú": "Lima",\n    "Chile": "Santiago",\n    "Argentina": "Buenos Aires"\n}\n\nfor pais, capital in capitales.items():\n    print(f"🇵🇪 La capital de {pais} es {capital}")\n\n# Solo valores\nprint("\\nCapitales:", list(capitales.values()))',
                description="Itera sobre claves, valores o ambos.",
            ),
            PyExample(
                title="Dict Comprehension",
                code="numeros = [1, 2, 3, 4, 5]\ncuadrados = {n: n**2 for n in numeros}\nprint(cuadrados)\n\n# Filtrar\npares_cuad = {n: n**2 for n in numeros if n % 2 == 0}\nprint(pares_cuad)",
                description="Crea diccionarios en una línea.",
            ),
        ],
        related=["listas", "funciones", "json"],
    ),
    PyTopic(
        id="oop",
        title="Programación Orientada a Objetos",
        category="Paradigmas",
        icon="🏛️",
        level="Intermedio",
        summary="Clases, objetos, herencia y encapsulación.",
        content=textwrap.dedent("""\
            La [bold]POO[/] organiza el código en [bold]clases[/] y [bold]objetos[/].

            [bold]Conceptos:[/]
              • [cyan]class[/]     → Plantilla para crear objetos
              • [cyan]__init__[/]  → Constructor (inicializa el objeto)
              • [cyan]self[/]      → Referencia al objeto actual
              • [cyan]herencia[/]  → Una clase hereda de otra
              • [cyan]encapsulación[/] → _atributo (privado por convención)
              • [cyan]@property[/] → Getter estilo atributo
        """),
        examples=[
            PyExample(
                title="Clase básica",
                code="class Perro:\n    def __init__(self, nombre, raza):\n        self.nombre = nombre\n        self.raza = raza\n    \n    def ladrar(self):\n        return f\"{self.nombre} dice: ¡Guau!\"\n    \n    def __str__(self):\n        return f\"{self.nombre} ({self.raza})\"\n\nmi_perro = Perro(\"Rex\", \"Pastor Alemán\")\nprint(mi_perro)\nprint(mi_perro.ladrar())",
                description="Define una clase con constructor y métodos.",
            ),
            PyExample(
                title="Herencia",
                code="class Animal:\n    def __init__(self, nombre):\n        self.nombre = nombre\n    def hacer_sonido(self):\n        pass\n\nclass Gato(Animal):\n    def hacer_sonido(self):\n        return f\"{self.nombre} dice: ¡Miau!\"\n\nclass Vaca(Animal):\n    def hacer_sonido(self):\n        return f\"{self.nombre} dice: ¡Muuu!\"\n\ngato = Gato(\"Whiskers\")\nvaca = Vaca(\"Lola\")\nprint(gato.hacer_sonido())\nprint(vaca.hacer_sonido())",
                description="Las subclases heredan y pueden sobrescribir métodos.",
            ),
        ],
        related=["funciones", "clases_avanzadas"],
    ),
    PyTopic(
        id="excepciones",
        title="Manejo de Excepciones",
        category="Fundamentos",
        icon="⚠️",
        level="Intermedio",
        summary="Captura y maneja errores con try/except.",
        content=textwrap.dedent("""\
            Las [bold]excepciones[/] son errores que ocurren durante la ejecución.
            Con [cyan]try/except[/] puedes manejarlas sin que el programa se detenga.

            [bold]Estructura:[/]
              [green]try[/]:
                  [dim]# código que puede fallar[/]
              [green]except[/] TipoError:
                  [dim]# qué hacer si ocurre ese error[/]
              [green]else[/]:
                  [dim]# código si NO hubo error[/]
              [green]finally[/]:
                  [dim]# código que SIEMPRE se ejecuta[/]

            [bold]Excepciones comunes:[/]
              • [cyan]ValueError[/]   → Valor inválido
              • [cyan]TypeError[/]    → Tipo incorrecto
              • [cyan]KeyError[/]     → Clave no existe en dict
              • [cyan]IndexError[/]   → Índice fuera de rango
              • [cyan]FileNotFoundError[/] → Archivo no existe
        """),
        examples=[
            PyExample(
                title="try/except básico",
                code="try:\n    numero = int(input(\"Dame un número: \"))\n    print(f\"El doble es {numero * 2}\")\nexcept ValueError:\n    print(\"❌ Eso no es un número válido\")\nelse:\n    print(\"✅ Conversión exitosa\")\nfinally:\n    print(\"👋 Gracias por participar\")",
                description="Captura errores de tipo específico.",
            ),
            PyExample(
                title="Múltiples excepciones",
                code="def dividir(a, b):\n    try:\n        resultado = a / b\n    except ZeroDivisionError:\n        return \"❌ No se puede dividir por cero\"\n    except TypeError:\n        return \"❌ Solo números, por favor\"\n    else:\n        return f\"✅ {a} / {b} = {resultado}\"\n\nprint(dividir(10, 2))\nprint(dividir(10, 0))\nprint(dividir(10, \"x\"))",
                description="Captura diferentes tipos de error por separado.",
            ),
        ],
        related=["funciones", "archivos"],
    ),
    PyTopic(
        id="archivos",
        title="Archivos y pathlib",
        category="IO",
        icon="📁",
        level="Intermedio",
        summary="Lee y escribe archivos usando pathlib y open().",
        content=textwrap.dedent("""\
            Trabaja con archivos usando [cyan]open()[/] o [cyan]pathlib[/].

            [bold]Modos de apertura:[/]
              • [cyan]'r'[/]  → Leer (por defecto)
              • [cyan]'w'[/]  → Escribir (sobrescribe)
              • [cyan]'a'[/]  → Agregar (append)
              • [cyan]'rb'[/] → Leer binario

            [bold]Context manager ([green]with[/]):[/]
              [green]with[/] open('archivo.txt', 'r') [green]as[/] f:
                  contenido = f.read()
              [dim]# se cierra automáticamente[/]
        """),
        examples=[
            PyExample(
                title="Escribir y leer",
                code="with open('mi_archivo.txt', 'w') as f:\n    f.write('Hola desde PyQuest!\\n')\n    f.write('Línea 2\\n')\n\nwith open('mi_archivo.txt', 'r') as f:\n    for linea in f:\n        print(f\"📄 {linea}\", end='')\n\n# Limpiar\nimport os\nos.remove('mi_archivo.txt')",
                description="Escribe y lee un archivo de texto.",
            ),
            PyExample(
                title="pathlib (moderno)",
                code="from pathlib import Path\n\nruta = Path('datos')\nruta.mkdir(exist_ok=True)\n\narchivo = ruta / 'notas.txt'\narchivo.write_text('Python es divertido!')\n\nprint(f\"Leído: {archivo.read_text()}\")\nprint(f\"Existe: {archivo.exists()}\")\n\n# Limpiar\narchivo.unlink()\nruta.rmdir()",
                description="pathlib es la forma moderna de manejar rutas.",
            ),
        ],
        related=["excepciones", "modulos"],
    ),
    # ─── NIVEL 3: Avanzado ───
    PyTopic(
        id="decoradores",
        title="Decoradores",
        category="Técnicas Avanzadas",
        icon="🎭",
        level="Avanzado",
        summary="Funciones que modifican otras funciones usando @sintax.",
        content=textwrap.dedent("""\
            Los [bold]decoradores[/] son funciones que envuelven otras funciones
            para extender su comportamiento sin modificar su código.

            [green]@mi_decorador[/]
            [green]def[/] mi_funcion():
                [dim]pass[/]

            Es equivalente a:
            [cyan]mi_funcion = mi_decorador(mi_funcion)[/]
        """),
        examples=[
            PyExample(
                title="Decorador simple",
                code="def medir_tiempo(func):\n    import time\n    def wrapper(*args, **kwargs):\n        inicio = time.time()\n        resultado = func(*args, **kwargs)\n        fin = time.time()\n        print(f\"⏱ {func.__name__} tardó {fin-inicio:.4f}s\")\n        return resultado\n    return wrapper\n\n@medir_tiempo\ndef calcular():  \n    total = sum(range(1000000))\n    return total\n\nresultado = calcular()\nprint(f\"Resultado: {resultado}\")",
                description="Mide el tiempo de ejecución de cualquier función.",
            ),
        ],
        related=["funciones", "closures"],
    ),
    PyTopic(
        id="generators",
        title="Generadores y yield",
        category="Técnicas Avanzadas",
        icon="♻️",
        level="Avanzado",
        summary="Funciones que producen una secuencia de valores bajo demanda.",
        content=textwrap.dedent("""\
            Los [bold]generadores[/] usan [cyan]yield[/] en vez de [cyan]return[/].
            Producen valores uno a uno, bajo demanda, ahorrando memoria.

            [bold]Diferencias:[/]
              • [cyan]return[/]  → Termina la función y retorna un valor
              • [cyan]yield[/]   → Pausa la función y retorna un valor
              • [cyan]next()[/]  → Reanuda el generador hasta el próximo yield
              • [cyan]yield from[/] → Delega a otro generador
        """),
        examples=[
            PyExample(
                title="Generador básico",
                code="def contar_hasta(n):\n    i = 1\n    while i <= n:\n        yield i\n        i += 1\n\nfor num in contar_hasta(5):\n    print(f\"🔢 {num}\")\n\n# También con next()\ngen = contar_hasta(3)\nprint(next(gen))  # 1\nprint(next(gen))  # 2\nprint(next(gen))  # 3",
                description="Yield produce valores uno a uno sin ocupar memoria.",
            ),
            PyExample(
                title="Generador infinito",
                code="def fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\nfib = fibonacci()\nfor _ in range(10):\n    print(next(fib), end=' ')\n# 0 1 1 2 3 5 8 13 21 34",
                description="Genera la secuencia infinita de Fibonacci.",
            ),
        ],
        related=["bucles", "funciones", "iteradores"],
    ),
    PyTopic(
        id="modulos",
        title="Módulos y Paquetes",
        category="Organización",
        icon="📦",
        level="Intermedio",
        summary="Organiza tu código en archivos reutilizables.",
        content=textwrap.dedent("""\
            Los [bold]módulos[/] son archivos [cyan].py[/] que puedes importar.
            Los [bold]paquetes[/] son carpetas con [cyan]__init__.py[/].

            [bold]Importar:[/]
              • [green]import[/] modulo
              • [green]from[/] modulo [green]import[/] funcion
              • [green]import[/] modulo [green]as[/] alias

            [bold]Si ejecutas el archivo directamente:[/]
              [green]if[/] [cyan]__name__[/] [green]==[/] [cyan]\"__main__\"[/]:
                  [dim]# código que solo corre al ejecutar directamente[/]
        """),
        examples=[
            PyExample(
                title="Importar y usar",
                code="import math\nimport random\nfrom datetime import datetime\n\nprint(f\"π = {math.pi:.4f}\")\nprint(f\"Aleatorio: {random.randint(1, 10)}\")\nprint(f\"Ahora: {datetime.now()}\")",
                description="Importa módulos de la biblioteca estándar.",
            ),
            PyExample(
                title="Tu propio módulo (simulado)",
                code="# Así se protege el código de ejecución al importar\ndef saludar():\n    return \"¡Hola desde el módulo!\"\n\nif __name__ == \"__main__\":\n    print(\"Esto solo se ve si ejecuto este archivo\")\n    print(saludar())\nelse:\n    print(\"✅ Módulo importado correctamente\")",
                description="Usa __name__ para controlar la ejecución.",
            ),
        ],
        related=["funciones", "archivos"],
    ),
    PyTopic(
        id="json",
        title="JSON",
        category="IO",
        icon="💾",
        level="Intermedio",
        summary="Guarda y carga datos estructurados con JSON.",
        content=textwrap.dedent("""\
            [bold]JSON[/] (JavaScript Object Notation) es el formato
            más popular para guardar/intercambiar datos.

            [bold]json[/] module:
              • [cyan]json.dumps()[/]  → dict/list → string JSON
              • [cyan]json.loads()[/]  → string JSON → dict/list
              • [cyan]json.dump()[/]   → dict/list → archivo
              • [cyan]json.load()[/]   → archivo → dict/list
        """),
        examples=[
            PyExample(
                title="JSON básico",
                code="import json\n\ndatos = {\n    \"nombre\": \"PyQuest\",\n    \"versión\": 1.0,\n    \"zonas\": [\"Variables\", \"Bucles\", \"Funciones\"],\n    \"activo\": True\n}\n\n# Convertir a string\njson_str = json.dumps(datos, indent=2)\nprint(\"📤 JSON:\")\nprint(json_str)\n\n# Convertir de vuelta a dict\nrecuperado = json.loads(json_str)\nprint(f\"\\n📥 Versión: {recuperado['versión']}\")",
                description="Convierte entre Python y JSON fácilmente.",
            ),
            PyExample(
                title="Guardar y cargar archivo",
                code="import json\n\n# Guardar\nconfig = {\"usuario\": \"dev\", \"tema\": \"oscuro\"}\nwith open('config.json', 'w') as f:\n    json.dump(config, f, indent=2)\n\n# Cargar\nwith open('config.json', 'r') as f:\n    cargado = json.load(f)\n\nprint(f\"Usuario: {cargado['usuario']}\")\nprint(f\"Tema: {cargado['tema']}\")\n\nimport os\nos.remove('config.json')",
                description="Persiste datos en archivos JSON.",
            ),
        ],
        related=["dicts", "archivos", "excepciones"],
    ),
    PyTopic(
        id="async",
        title="Async/Await",
        category="Técnicas Avanzadas",
        icon="⏳",
        level="Avanzado",
        summary="Programación asíncrona con async/await para I/O concurrente.",
        content=textwrap.dedent("""\
            [bold]async/await[/] permite ejecutar operaciones I/O
            en simultáneo sin necesidad de threads.

            [bold]Conceptos:[/]
              • [cyan]async def[/]   → Define una función asíncrona (corrutina)
              • [cyan]await[/]       → Espera una operación asíncrona
              • [cyan]asyncio.run()[/] → Punto de entrada
              • [cyan]asyncio.gather()[/] → Ejecuta varias tareas en paralelo
        """),
        examples=[
            PyExample(
                title="Async básico",
                code="import asyncio\n\nasync def tarea(nombre, segundos):\n    print(f\"  ▶ {nombre} iniciando...\")\n    await asyncio.sleep(segundos)\n    print(f\"  ✔ {nombre} completada\")\n    return f\"{nombre} terminó\"\n\nasync def main():\n    # Ejecuta 3 tareas en paralelo\n    resultados = await asyncio.gather(\n        tarea(\"Tarea 1\", 2),\n        tarea(\"Tarea 2\", 1),\n        tarea(\"Tarea 3\", 3),\n    )\n    for r in resultados:\n        print(f\"📬 {r}\")\n\nasyncio.run(main())",
                description="async/await para operaciones concurrentes (simulado con sleep).",
            ),
        ],
        related=["funciones", "excepciones", "modulos"],
    ),
    PyTopic(
        id="testing",
        title="Testing con pytest",
        category="Herramientas",
        icon="🧪",
        level="Avanzado",
        summary="Escribe pruebas automatizadas para tu código.",
        content=textwrap.dedent("""\
            [bold]Testing[/] es escribir código que verifica que tu código funciona.

            [bold]assert[/] — la base de todo test:
              [green]assert[/] condicion, [red]\"Mensaje si falla\"[/]

            [bold]pytest[/] hace testing fácil:
              • Funciones que empiezan con [cyan]test_[/]
              • Usa [cyan]assert[/] normal de Python
              • [cyan]@pytest.fixture[/] para datos compartidos
              • [cyan]@pytest.mark.parametrize[/] para múltiples casos
        """),
        examples=[
            PyExample(
                title="Test con assert",
                code="def sumar(a, b):\n    return a + b\n\ndef restar(a, b):\n    return a - b\n\n# Tests\nassert sumar(2, 3) == 5, \"2+3 debe ser 5\"\nassert sumar(-1, 1) == 0, \"-1+1 debe ser 0\"\nassert restar(10, 7) == 3, \"10-7 debe ser 3\"\nassert restar(0, 0) == 0, \"0-0 debe ser 0\"\n\nprint(\"✅ Todos los tests pasaron\")",
                description="assert verifica que una condición sea verdadera.",
            ),
            PyExample(
                title="Test parametrizado",
                code="def es_par(n):\n    return n % 2 == 0\n\ncasos = [\n    (2, True),\n    (3, False),\n    (0, True),\n    (-4, True),\n    (7, False),\n]\n\nfor numero, esperado in casos:\n    resultado = es_par(numero)\n    assert resultado == esperado, f\"{numero} falló: esperado {esperado}, recibido {resultado}\"\n    print(f\"  ✓ {numero} → {'par' if resultado else 'impar'}\")\n\nprint(\"✅ Todos los tests parametrizados pasaron\")",
                description="Prueba múltiples casos con un bucle.",
            ),
        ],
        related=["funciones", "excepciones", "bucles"],
    ),
    PyTopic(
        id="sets",
        title="Sets y Tuplas",
        category="Estructuras de Datos",
        icon="🔷",
        level="Intermedio",
        summary="Colecciones: sets (sin duplicados) y tuplas (inmutables).",
        content=textwrap.dedent("""\
            [bold]Sets[/] ([cyan]{1, 2, 3}[/]):[/]
              • No tienen duplicados
              • No tienen orden
              • Operaciones: [cyan]|[/] unión, [cyan]&[/] intersección, [cyan]-[/] diferencia

            [bold]Tuplas[/] ([cyan](1, 2, 3)[/]):[/]
              • Inmutables (no se pueden modificar)
              • Útiles para datos que no deben cambiar
              • Se pueden usar como claves de diccionario
        """),
        examples=[
            PyExample(
                title="Operaciones con sets",
                code="a = {1, 2, 3, 4, 5}\nb = {4, 5, 6, 7, 8}\n\nprint(f\"Unión: {a | b}\")\nprint(f\"Intersección: {a & b}\")\nprint(f\"Diferencia (a-b): {a - b}\")\nprint(f\"Diferencia simétrica: {a ^ b}\")\n\n# Eliminar duplicados\nnumeros = [1, 2, 2, 3, 3, 3, 4]\nunicos = list(set(numeros))\nprint(f\"Únicos: {unicos}\")",
                description="Sets para operaciones de conjuntos y eliminar duplicados.",
            ),
            PyExample(
                title="Tuplas inmutables",
                code='# Tuplas no se pueden modificar\npunto = (3, 4)\nx, y = punto\nprint(f"Coordenada: ({x}, {y})")\n\ndef dividir_con_residuo(a, b):\n    return (a // b, a % b)  # tupla como retorno múltiple\n\ncociente, residuo = dividir_con_residuo(10, 3)\nprint(f"10/3: cociente={cociente}, residuo={residuo}")',
                description="Tuplas para datos inmutables y retornos múltiples.",
            ),
        ],
        related=["listas", "dicts", "bucles"],
    ),
    PyTopic(
        id="comprehensions",
        title="Comprensiones (List, Dict, Set)",
        category="Técnicas Avanzadas",
        icon="⚡",
        level="Intermedio",
        summary="Crea colecciones en una línea con sintaxis compacta.",
        content=textwrap.dedent("""\
            Las [bold]comprensiones[/] crean colecciones de forma elegante.

            [bold]List comprehension:[/]
              [cyan][expr for item in iterable if cond][/]

            [bold]Dict comprehension:[/]
              [cyan]{key: val for item in iterable if cond}[/]

            [bold]Set comprehension:[/]
              [cyan]{expr for item in iterable}[/]

            [bold]Generator expression:[/]
              [cyan](expr for item in iterable)[/]  [dim]# no crea la lista[/]
        """),
        examples=[
            PyExample(
                title="List vs Generator",
                code="# List comprehension (ocupa memoria)\ncuadrados_lista = [x**2 for x in range(10)]\nprint(f\"Lista: {cuadrados_lista}\")\n\n# Generator expression (bajo demanda)\ncuadrados_gen = (x**2 for x in range(10))\nprint(f\"Generator: {list(cuadrados_gen)}\")\n\n# Con filtro\npares = [x for x in range(20) if x % 2 == 0]\nprint(f\"Pares: {pares}\")",
                description="List comprehension crea toda la lista; generator expression la genera bajo demanda.",
            ),
            PyExample(
                title="Anidada y múltiples condiciones",
                code="# Matriz transpuesta\nmatriz = [\n    [1, 2, 3],\n    [4, 5, 6],\n]\ntranspuesta = [[fila[i] for fila in matriz] for i in range(3)]\nprint(f\"Original: {matriz}\")\nprint(f\"Transpuesta: {transpuesta}\")\n\n# Múltiples fors\npares = [(x, y) for x in range(3) for y in range(3) if x != y]\nprint(f\"Pares: {pares}\")",
                description="Comprensiones anidadas y con múltiples condiciones.",
            ),
        ],
        related=["listas", "dicts", "sets", "bucles"],
    ),
]


CATEGORIES: dict[str, list[PyTopic]] = {}
for topic in TOPICS:
    CATEGORIES.setdefault(topic.category, []).append(topic)


def get_topic(topic_id: str) -> PyTopic | None:
    for t in TOPICS:
        if t.id == topic_id:
            return t
    return None


def search_topics(query: str) -> list[PyTopic]:
    q = query.lower()
    results = []
    for t in TOPICS:
        if q in t.title.lower() or q in t.summary.lower() or q in t.id.lower():
            results.append(t)
    return results


def render_topic_list():
    console.clear()
    title = Text("📚  Documentación Interactiva de Python", style="bold cyan")
    console.print(Align.center(title))
    console.print()

    for cat, topics in CATEGORIES.items():
        header = Text(f"\n  ▸ {cat}", style=f"bold yellow")
        console.print(header)
        for t in topics:
            lvl_colors = {"Principiante": "green", "Intermedio": "yellow", "Avanzado": "red"}
            lvl_color = lvl_colors.get(t.level, "white")
            console.print(
                f"    {t.icon}  [bold white]{t.id}[/]  —  {t.title}"
                f"  [{lvl_color}]({t.level})[/]"
            )
            console.print(f"       [dim]{t.summary}[/]")

    console.print()
    console.print("  [bold cyan]/docs <tema>[/]  — Ver un tema específico")
    console.print("  [bold cyan]/docs buscar <q>[/] — Buscar en la documentación")
    console.print("  [bold cyan]/docs ejecutar <tema>[/] — Ver y ejecutar ejemplos")
    console.print()


def render_topic_detail(topic_id: str):
    topic = get_topic(topic_id)
    if topic is None:
        console.print(f"[red]❌ Tema '{topic_id}' no encontrado.[/]")
        return

    xp_gained = mark_viewed(topic_id)
    tp = get_topic_progress(topic_id)
    status_icon = STATUS_ICONS.get(tp.status, "📦")
    status_label = STATUS_LABELS.get(tp.status, "Nuevo")

    console.clear()
    lvl_colors = {"Principiante": "green", "Intermedio": "yellow", "Avanzado": "red"}
    lvl_color = lvl_colors.get(topic.level, "white")
    status_color = {"new": "dim", "learning": "cyan", "practiced": "green", "mastered": "yellow"}.get(tp.status, "dim")

    header = Text()
    header.append(f" {topic.icon}  ", style="bold")
    header.append(topic.title, style="bold cyan")
    header.append(f"  [{lvl_color}]({topic.level})[/]")
    header.append(f"  [{status_color}]{status_icon} {status_label}[/]")
    header.append(f"  [dim]+{tp.xp_earned} XP[/]")
    console.print(Panel(header, border_style="cyan", box=box.HEAVY))
    console.print()
    if xp_gained:
        console.print(f"[dim]  +{xp_gained} XP por explorar este tema[/]")
        console.print()

    console.print(Text.from_markup(topic.content))
    console.print()

    if topic.examples:
        console.print(Text("  💻  EJEMPLOS INTERACTIVOS", style="bold yellow"))
        console.print("  [dim]Escribe el número del ejemplo para ejecutarlo, o Enter para volver.[/]")
        console.print()

        for i, ex in enumerate(topic.examples, 1):
            panel = Panel(
                Text(ex.code, style="green"),
                title=f"Ejemplo {i}: {ex.title}",
                border_style="bright_green",
                box=box.SQUARE,
                padding=(0, 1),
            )
            console.print(panel)
            if ex.description:
                console.print(f"   [dim]{ex.description}[/]")
            console.print()

        _interactive_examples(topic)

    if topic.related:
        console.print()
        console.print(Text("  🔗  TEMAS RELACIONADOS", style="bold cyan"))
        related_names = []
        for r in topic.related:
            rt = get_topic(r)
            if rt:
                related_names.append(f"{rt.icon} [cyan]/docs {rt.id}[/] — {rt.title}")
        for rn in related_names:
            console.print(f"     • {rn}")


def _interactive_examples(topic: PyTopic):
    console.print("  [dim]Número del ejemplo para ejecutar, o Enter para salir:[/]")
    choice = console.input("  [bold]>> [/]").strip()

    if not choice:
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(topic.examples):
            ex = topic.examples[idx]
            console.clear()
            console.print(Panel(
                Text(f"Ejecutando: {ex.title}", style="bold cyan"),
                border_style="cyan",
            ))
            console.print()
            console.print(Text(ex.code, style="green"))
            console.print()

            result = execute_code(ex.code, mode="script", timeout=5)

            if result.exit_code == 0:
                ex_xp = mark_example_run(topic.id, ex.title)
                console.print(Text("  ✅  SALIDA:", style="bold green"))
                console.print(Panel(
                    Text(result.stdout if result.stdout else "(sin salida)", style="white"),
                    border_style="green",
                ))
                if ex_xp:
                    console.print(f"[dim green]  +{ex_xp} XP por ejemplo completado[/]")
            else:
                console.print(Text("  ❌  ERROR:", style="bold red"))
                console.print(Panel(
                    Text(result.stderr if result.stderr else "Error desconocido", style="red"),
                    border_style="red",
                ))

            console.print()
            console.print("[dim]Presiona Enter para volver al tema...[/]")
            console.input()
            render_topic_detail(topic.id)
        else:
            console.print(f"[red]Número inválido. Elige 1-{len(topic.examples)}[/]")
            _interactive_examples(topic)
    except ValueError:
        pass


def show_docs(args: str = ""):
    if not args:
        render_topic_list()
        topic_id = console.input("[bold]¿Qué tema quieres explorar? [/]").strip().lower()
        if topic_id:
            show_docs(topic_id)
        return

    parts = args.strip().split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd == "buscar" and len(parts) > 1:
        results = search_topics(parts[1])
        if not results:
            console.print(f"[yellow]No se encontraron temas para '{parts[1]}'[/]")
            return
        console.print(f"\n[bold cyan]Resultados para '{parts[1]}':[/]")
        for t in results:
            console.print(f"  {t.icon}  [cyan]/docs {t.id}[/]  —  {t.title}")
        console.print()
        topic_id = console.input("[bold]Elige un tema: [/]").strip()
        if topic_id:
            render_topic_detail(topic_id)
        return

    if cmd == "ejecutar" and len(parts) > 1:
        topic = get_topic(parts[1])
        if not topic:
            console.print(f"[red]❌ Tema '{parts[1]}' no encontrado.[/]")
            return
        render_topic_detail(parts[1])
        return

    topic = get_topic(cmd)
    if topic:
        render_topic_detail(cmd)
    else:
        console.print(f"[red]❌ Tema '{cmd}' no encontrado.[/]")
        console.print("[dim]Usa /docs para ver todos los temas disponibles.[/]")


def show_playground():
    """REPL interactivo dentro del juego para experimentar con código."""
    console.clear()
    console.print(Panel(
        Text("🐍  Python Playground  —  Experimenta libremente", style="bold cyan"),
        border_style="cyan",
        box=box.HEAVY,
    ))
    console.print("[dim]Escribe código Python. Se ejecutará al presionar Ctrl+D[/]")
    console.print("[dim]Escribe /docs para ver la documentación interactiva[/]")
    console.print("[dim]Escribe /salir para volver al juego[/]")
    console.print()

    lines = []
    while True:
        try:
            line = input("  >>> " if not lines else "  ... ")
            if line.strip().lower() == "/salir":
                break
            if line.strip().lower() == "/docs":
                show_docs()
                console.print("\n[dim]Continúa en el playground o escribe /salir:[/]")
                continue
            if line.strip().lower() == "/limpiar":
                console.clear()
                lines = []
                continue
            lines.append(line)
        except EOFError:
            if lines:
                code = "\n".join(lines)
                console.print("[dim]⏳ Ejecutando...[/]")
                result = execute_code(code, mode="script", timeout=5)
                if result.exit_code == 0:
                    if result.stdout:
                        console.print(Text(result.stdout, style="green"))
                else:
                    console.print(Panel(
                        Text(result.stderr or "Error", style="red"),
                        border_style="red",
                    ))
                lines = []
                console.print()
            else:
                break
        except KeyboardInterrupt:
            console.print("\n[yellow]Playground cerrado[/]")
            break
