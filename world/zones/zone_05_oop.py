from world.zones import Zone, Mission, TestCase


zone = Zone(
    id=5,
    name="La Torre",
    story_intro=(
        "La Torre de la POO se alza imponente.\n"
        "Cada piso es una clase, cada puerta un método.\n"
        "El arquitecto te desafía a construir tu propia clase."
    ),
    missions=[
        Mission(
            num=1, title="Clase Héroe",
            description="Define una clase `Heroe` con __init__ que reciba nombre y vida. Crea una instancia y muestra su nombre.",
            execution_mode="script",
            code_template="class Heroe:\n    def __init__(self, nombre, vida):\n        self.nombre = nombre\n        self.vida = vida\n\nh = Heroe('Aragon', 100)\nprint(h.nombre)",
            test_cases=[TestCase(input="", expected="Aragon")],
            hints=["__init__ es el constructor de la clase", "self representa la instancia actual"],
        ),
        Mission(
            num=2, title="Métodos de Batalla",
            description="Agrega a Heroe el método `atacar(self, otro)` que reduzca vida de otro en 10. Crea dos héroes, haz que uno ataque al otro y muestra la vida restante.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="90")],
            hints=["self.vida -= 10 reduce la vida", "otro es otra instancia de Heroe"],
        ),
        Mission(
            num=3, title="Herencia Mágica",
            description="Define `Mago(Heroe)` con __init__ que agregue `mana`. Crea un mago con mana=50 y muestra su mana.",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="50")],
            hints=["class Mago(Heroe): hereda de Heroe", "super().__init__(nombre, vida) llama al constructor padre"],
        ),
        Mission(
            num=4, title="Dunder Power",
            description="Agrega __str__ a Heroe que retorne 'Heroe: X (Vida: Y)'. Muestra un héroe con print().",
            execution_mode="script",
            test_cases=[TestCase(input="", expected="Heroe:")],
            hints=["__str__ debe retornar un string", "Se llama automáticamente con print()"],
        ),
        Mission(
            num=5, title="Boss: Sistema de Inventario",
            description="Crea clase `Item` (nombre, peso) y clase `Inventario` con lista de items, método `agregar(item)`, método `peso_total()`. Usa esta prueba:\n\nitem1 = Item('Espada', 3.5)\nitem2 = Item('Escudo', 2.0)\nitem3 = Item('Poción', 0.5)\ninv = Inventario()\ninv.agregar(item1)\ninv.agregar(item2)\ninv.agregar(item3)\nprint(inv.peso_total())",
            execution_mode="script",
            code_template="class Item:\n    def __init__(self, nombre, peso):\n        self.nombre = nombre\n        self.peso = peso\n\nclass Inventario:\n    def __init__(self):\n        self.items = []\n    def agregar(self, item):\n        self.items.append(item)\n    def peso_total(self):\n        return sum(item.peso for item in self.items)\n\nitem1 = Item('Espada', 3.5)\nitem2 = Item('Escudo', 2.0)\nitem3 = Item('Poción', 0.5)\ninv = Inventario()\ninv.agregar(item1)\ninv.agregar(item2)\ninv.agregar(item3)\nprint(inv.peso_total())",
            test_cases=[TestCase(input="", expected="6.0")],
            hints=["Usa una lista para almacenar items", "sum(item.peso for item in items) calcula el total"],
        ),
    ],
)
