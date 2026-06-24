"""Ejemplo: Programación asíncrona con async/await."""

import asyncio


async def tarea(nombre, segundos):
    print(f"  ▶ {nombre} iniciando...")
    await asyncio.sleep(segundos)
    print(f"  ✔ {nombre} completada")
    return f"{nombre} terminó"


async def main():
    resultados = await asyncio.gather(
        tarea("Tarea 1", 2),
        tarea("Tarea 2", 1),
        tarea("Tarea 3", 3),
    )
    for r in resultados:
        print(f"📬 {r}")


asyncio.run(main())
