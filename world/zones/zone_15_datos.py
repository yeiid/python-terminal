from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=15,
    name="El Banco de Datos",
    story_intro=(
        "En las profundidades del Banco de Datos reposan estructuras olvidadas.\n"
        "Colas, pilas, árboles y grafos esperan ser reimplementados.\n"
        "¿Podrás recuperar el algoritmo perdido?"
    ),
    missions=[
        Mission(
            num=1, title="Pila de la Memoria",
            description="Implementa una clase `Pila` con métodos push(item), pop() y is_empty(). Prueba: push 1, push 2, pop (debe mostrar 2).",
            execution_mode="script",
            code_template="class Pila:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0\n\np = Pila()\np.push(1)\np.push(2)\nprint(p.pop())",
            test_cases=[TestCase(input="", expected="2")],
            hints=["pop() sin índice saca el último elemento", "is_empty() retorna True si la lista está vacía"],
        ),
        Mission(
            num=2, title="Cola del Sistema",
            description="Implementa una clase `Cola` con métodos enqueue(item), dequeue() y size(). Prueba: encola 'a', 'b', dequeue (debe mostrar 'a').",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="a")],
            hints=["Usa collections.deque para una cola eficiente", "popleft() para dequeue"],
        ),
        Mission(
            num=3, title="Conjuntos Mágicos",
            description="Dadas dos listas A = [1, 2, 3, 4] y B = [3, 4, 5, 6], muestra: la unión, la intersección y la diferencia A - B.",
            execution_mode="script",
            code_template="A = [1, 2, 3, 4]\nB = [3, 4, 5, 6]\nunion = set(A) | set(B)\ninterseccion = set(A) & set(B)\ndiferencia = set(A) - set(B)\nprint(sorted(union))\nprint(sorted(interseccion))\nprint(sorted(diferencia))",
            test_cases=[TestCase(input="", expected="[1, 2, 3, 4, 5, 6]\n[3, 4]\n[1, 2]")],
            hints=["Convierte a set() para operaciones de conjuntos", "sorted() para ordenar el resultado"],
        ),
        Mission(
            num=4, title="Árbol Binario Simple",
            description="Define una clase `Nodo` con valor, izquierda y derecha. Crea un árbol de 3 niveles y haz un recorrido in-order que muestre los valores.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["Nodo izquierdo tiene un valor menor, derecho mayor", "In-order: izquierdo → raíz → derecho"],
        ),
        Mission(
            num=5, title="Boss: Grafo Social",
            description="Implementa un grafo simple usando dict de listas de adyacencia.\nDefine: agregar_amigo(persona1, persona2) y mostrar_red(persona) que muestre sus conexiones.\nCrea una red con 4 personas y muestra la red de 'Ana'.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="")],
            hints=["Usa un dict[str, list[str]]", "Cada arista se agrega en ambos sentidos (no dirigido)"],
        ),
    ],
)
