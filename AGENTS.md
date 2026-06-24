# PyQuest — Guía para Agentes de IA

## Estructura del proyecto

```
pyquest/
├── main.py                  # Entry point, CLI, game loop
├── engine/                  # Motor del juego
│   ├── acts.py              # Sistema de Actos (I, II, III, ∞)
│   ├── battlepass.py        # Battle pass tiers + collection objects
│   ├── collection.py        # Collectible object system
│   ├── console.py           # Rich Console singleton
│   ├── curriculum.py        # Topic learning progress tracking
│   ├── executor.py          # Sandboxed code execution (subprocess)
│   ├── menu.py              # Tab menu with prompt_toolkit
│   ├── panel.py             # Interactive learning panel (/temas)
│   ├── profile.py           # Player profile with 5 tabs
│   ├── pyhelp.py            # Interactive Python docs (~18 topics)
│   ├── renderer.py          # UI rendering orchestrator (uses ui/)
│   ├── schema.py            # Zone file validation + template generation
│   ├── state.py             # GameState dataclass (persistence, XP, achievements)
│   └── validator.py         # Code validation against test cases
├── ui/                      # UI system (reusable components)
│   ├── responsive.py        # Termux/width detection, responsive config
│   ├── themes.py            # Theme system (default, termux, high_contrast)
│   ├── components.py        # Shared UI components (headers, bars, panels)
│   └── indentation.py       # Indented output formatting for validation
├── world/                   # Zone definitions and map
│   ├── map.py               # 15 zone definitions + show_map()
│   ├── discovery.py         # Dynamic zone loading from world/zones/
│   └── zones/               # 15 zone files (zone_01 to zone_15)
├── assets/
│   ├── ascii/logo.txt       # ASCII art logo
│   └── designs/             # Theme and border definitions
│       ├── themes/          # default.py, termux.py, high_contrast.py
│       └── borders/         # minimal.py (ASCII-only borders)
├── tests/                   # Test suite (unittest + pytest)
│   ├── test_acts.py through test_validator.py (15 files)
│   ├── test_responsive.py   # NEW: responsive system tests
│   ├── test_indentation.py  # NEW: indentation tests
│   ├── test_main.py         # NEW: game loop tests (mock input)
│   ├── test_profile.py      # NEW: profile tab tests
│   ├── test_panel.py        # NEW: learning panel tests
│   └── test_zones/
│       └── test_zone_validity.py  # NEW: validates ALL zones
├── examples/                # Runnable example scripts
│   ├── basics/              # 01_variables, 02_strings, etc.
│   ├── intermediate/        # 01_oop, 02_decorators
│   └── advanced/            # 01_async
├── data/                    # Persisted game state (JSON)
├── setup_termux.sh          # Termux auto-installer
├── pyproject.toml           # Project config + deps
└── README.md
```

## Reglas importantes

1. **UI components** están en `ui/`, no en `engine/`. `engine/renderer.py` orquesta la UI.
2. **Responsive**: Siempre importar `from ui.responsive import responsive` para detección de ancho/termux.
3. **Console**: Crear consola local con `Console(highlight=False)` en módulos UI para evitar imports circulares.
4. **Tests**: Usar unittest. Los tests de zonas validan TODAS las zonas automáticamente.
5. **Test cases**: TODAS las misiones deben tener `expected` concreto (no vacío) en sus TestCase.

## Comandos

- `python3 main.py` — Jugar
- `python3 -m pytest tests/` — Ejecutar todos los tests
- `python3 tests/run_all.py` — Test runner alternativo
- `python3 -m pytest tests/test_zones/test_zone_validity.py -v` — Validar zonas

## Convenciones de código

- No añadir comentarios a menos que se solicite explícitamente
- Usar Rich para toda la UI, pero evitar imports circulares
- Los módulos `ui/` crean su propio `Console` en vez de importar `engine.console`
- Los temas se registran en `ui/themes.py` y se cargan desde `assets/designs/themes/`
