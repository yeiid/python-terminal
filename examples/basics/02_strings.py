"""Ejemplo: Strings y métodos de texto."""


texto = "  hola Python  "
print(texto.strip())
print(texto.upper())
print(texto.replace("Python", "Mundo"))
print(texto.split())

# f-strings
nombre = "Carlos"
lenguaje = "Python"
edad = 30
mensaje = f"{nombre} programa en {lenguaje} desde hace {edad} años"
print(mensaje)

# Slicing
texto = "Python"
print(texto[0])
print(texto[-1])
print(texto[0:3])
print(texto[::-1])
