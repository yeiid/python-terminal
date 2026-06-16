from world.zones import Zone, Mission


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
            example="class Heroe:\n    def __init__(self, nombre, vida):\n        self.nombre = nombre\n        self.vida = vida\n\nh = Heroe('Aragon', 100)\nprint(h.nombre)",
            validation_fn=lambda out, err: (out == "Aragon", "Debe mostrar 'Aragon'"),
        ),
        Mission(
            num=2, title="Métodos de Batalla",
            description="Agrega a Heroe el método `atacar(self, otro)` que reduzca vida de otro en 10. Crea dos héroes, haz que uno ataque al otro y muestra la vida restante.",
            validation_fn=lambda out, err: ("90" in out, "Vida restante debe ser 90"),
        ),
        Mission(
            num=3, title="Herencia Mágica",
            description="Define `Mago(Heroe)` con __init__ que agregue `mana`. Crea un mago con mana=50 y muestra su mana.",
            validation_fn=lambda out, err: ("50" in out, "Mana debe ser 50"),
        ),
        Mission(
            num=4, title="Dunder Power",
            description="Agrega __str__ a Heroe que retorne 'Heroe: X (Vida: Y)'. Muestra un héroe con print().",
            validation_fn=lambda out, err: ("Heroe:" in out and "Vida:" in out, "Formato: 'Heroe: X (Vida: Y)'"),
        ),
        Mission(
            num=5, title="Boss: Sistema de Inventario",
            description="Crea clase `Item` (nombre, peso) y clase `Inventario` con lista de items, método `agregar(item)`, método `peso_total()`. Carga 3 items variados y muestra el peso total.",
            validation_fn=lambda out, err: (True, ""),
        ),
    ],
)
