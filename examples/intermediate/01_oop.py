"""Ejemplo: Programación Orientada a Objetos."""


class Perro:
    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza

    def ladrar(self):
        return f"{self.nombre} dice: ¡Guau!"

    def __str__(self):
        return f"{self.nombre} ({self.raza})"


mi_perro = Perro("Rex", "Pastor Alemán")
print(mi_perro)
print(mi_perro.ladrar())


class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    def hacer_sonido(self):
        pass


class Gato(Animal):
    def hacer_sonido(self):
        return f"{self.nombre} dice: ¡Miau!"


gato = Gato("Whiskers")
print(gato.hacer_sonido())
