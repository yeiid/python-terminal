"""Ejemplo: Decoradores."""


def medir_tiempo(func):
    import time
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"⏱ {func.__name__} tardó {fin - inicio:.4f}s")
        return resultado
    return wrapper


@medir_tiempo
def calcular():
    total = sum(range(1000000))
    return total


resultado = calcular()
print(f"Resultado: {resultado}")
