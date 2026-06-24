"""Ejemplo: Condicionales if/elif/else."""


edad = 18
if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")

# Múltiples condiciones
nota = 85
if nota >= 90:
    print("Excelente")
elif nota >= 70:
    print("Bien")
elif nota >= 50:
    print("Suficiente")
else:
    print("Necesitas mejorar")

# Operadores lógicos
edad = 25
tiene_licencia = True
if edad >= 18 and tiene_licencia:
    print("Puedes conducir")
elif edad >= 18 and not tiene_licencia:
    print("Saca tu licencia primero")
else:
    print("Eres muy joven para conducir")
