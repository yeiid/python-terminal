# PyQuest – Terminal RPG

## Visión general del proyecto

**PyQuest** es un juego de rol (RPG) que se ejecuta directamente en la terminal y está pensado como una herramienta didáctica para aprender Python. Cada zona del juego está compuesta por misiones que el jugador resuelve escribiendo fragmentos de código Python. El juego valida la salida y premia al jugador con experiencia (XP). Además, los jugadores pueden crear sus propias zonas mediante plantillas, lo que permite que el juego evolucione de forma colaborativa.

### Estado actual
- **Jugabilidad completa** para las zonas predefinidas (1 a 13). El bucle principal permite pasar de zona en zona, ejecutar misiones, obtener hints, saltar misiones y guardar el progreso.
- **Editor de zonas** integrado: mediante el comando `/crear` se genera una plantilla (`zone_template.py`) que el usuario puede editar y colocar en `world/zones/`.
- **Validador** que revisa la sintaxis y lógica de una zona personalizada (`--validate`).
- **Persistencia** del estado del juego (`GameState`) en archivo JSON.
- **Interfaz enriquecida** con Rich (colores, paneles, inputs) para una experiencia de terminal atractiva.
- **Sistema de logros y recompensas** (XP, pistas, logros por zona y por misión).

## Estructura del proyecto
```
pyquest/
├─ .git/                # Información del repositorio Git
├─ .gitignore           # Archivos a excluir del control de versiones
├─ .venv/               # Entorno virtual (opcional)
├─ assets/              # Recursos estáticos (ASCII art, etc.)
│   └─ ascii/           # Imágenes ASCII usadas por el juego
├─ data/                # Datos estáticos (p. ej. zonas predefinidas)
├─ engine/              # Núcleo del juego
│   ├─ __init__.py
│   ├─ acts.py          # Definición de actos (actos) y transiciones
│   ├─ executor.py      # Ejecuta el código del jugador en sandbox
│   ├─ profile.py       # Gestión de perfil y estadísticas
│   ├─ renderer.py      # Renderizado de pantalla con Rich
│   ├─ schema.py        # Esquemas de validación de zona
│   ├─ state.py         # Modelo de estado del juego
│   └─ validator.py     # Validación de archivos de zona
├─ world/               # Definiciones de zonas y mapa
│   ├─ __init__.py
│   └─ zones/           # (creado por el usuario) archivos .py de zonas
├─ zone_template.py     # Plantilla base para crear una zona nueva
├─ main.py              # Entrada del programa, CLI y bucle principal
├─ pyproject.toml       # Configuración de Poetry / dependencias
└─ README.md            # ← Este archivo
```

## Cómo ejecutar el juego
```bash
# Crear y activar entorno virtual (opcional)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # o usar Poetry

# Ejecutar el juego
python main.py
```

Opciones útiles:
- `--validate <ruta>` – valida una zona personalizada.
- `--template` – genera `zone_template.py` para iniciar una nueva zona.

## Contribuir
1. Fork del repositorio.
2. Crear una nueva rama `feature/nueva-zona`.
3. Añadir o modificar código.
4. Ejecutar `python main.py --validate world/zones/mi_zona.py` para asegurarse de que la zona es válida.
5. Abrir Pull Request.

---

*Este README se generó automáticamente por Antigravity, el asistente de codificación IA.*
