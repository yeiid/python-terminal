"""Ejemplo: Bucles for y while."""


# for básico
for i in range(5):
    print(f"Iteración {i}")

# Recorrer lista
lenguajes = ["Python", "Java", "JavaScript", "Go"]
for lang in lenguajes:
    if lang == "Python":
        print(f"{lang} - ¡El mejor!")
    else:
        print(lang)

# while con break
contador = 0
while True:
    contador += 1
    print(f"Intento {contador}")
    if contador >= 3:
        print("¡Listo!")
        break
