#!/usr/bin/env python3
"""PyQuest — Terminal RPG para aprender Python.

Uso:
  python main.py               # Jugar
  python main.py --validate ruta/a/mi_zona.py  # Validar zona creada
  python main.py --template    # Generar template de zona
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.renderer import (
    console, show_title_screen, make_header, render_story,
    render_mission, render_result, show_commands, render_meta_moment,
    render_zone_creator_intro,
)
from engine.profile import show_profile
from engine.acts import get_act, render_act_transition, ACTS
from engine.schema import validate_zone_file, generate_template
from engine.executor import execute_code
from engine.validator import validate
from engine.state import GameState
from world.map import show_map, get_zone
from world import ZONE_CLASSES


def show_help():
    show_commands()
    console.input("\n[dim]Presiona Enter para continuar...[/]")


def handle_command(cmd: str, state: GameState) -> bool:
    cmd = cmd.strip().lower()
    if cmd == "/perfil":
        show_profile(state)
        return True
    elif cmd == "/mapa":
        show_map(state.unlocked_zones)
        console.input("\n[dim]Presiona Enter para continuar...[/]")
        return True
    elif cmd == "/acto":
        act = get_act(state.unlocked_zones)
        render_act_transition(act)
        return True
    elif cmd == "/crear":
        template = generate_template(state.player_name)
        path = Path("world/zones") / f"zone_13_{state.player_name.lower()}_zone.py"
        path.write_text(template)
        console.print(f"[green]✓ Template creado: {path}[/]")
        console.print("[dim]Edítalo y luego el juego lo descubrirá automáticamente.[/]")
        console.input("[dim]Presiona Enter para continuar...[/]")
        return True
    elif cmd.startswith("/validar"):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            console.print("[red]Usa: /validar ruta/al/archivo.py[/]")
            return True
        errors = validate_zone_file(parts[1])
        if errors:
            console.print("[red]Errores de validación:[/]")
            for e in errors:
                console.print(f"  ✗ {e}")
        else:
            console.print("[green]✓ Zona válida. Se integrará al juego automáticamente.[/]")
        console.input("[dim]Presiona Enter para continuar...[/]")
        return True
    elif cmd == "/ayuda":
        show_help()
        return True
    elif cmd == "/salir":
        state.save()
        console.print("\n[bold yellow]Juego guardado. ¡Hasta luego, dev![/]")
        sys.exit(0)
    return False


def get_multiline_input(state: GameState) -> str | None:
    lines = []
    console.print("[dim](Escribe código o escribe /comando  •  Ctrl+D para enviar  •  Ctrl+C para salir)[/]")
    first_line = console.input("[bold green]  >>> [/]")
    if first_line.startswith("/"):
        if handle_command(first_line, state):
            return ""
        return ""

    lines.append(first_line)
    try:
        while True:
            line = input("  ... ")
            lines.append(line)
    except EOFError:
        pass
    except KeyboardInterrupt:
        state.save()
        console.print("\n[bold yellow]Juego guardado. ¡Hasta luego, dev![/]")
        sys.exit(0)

    return "\n".join(lines)


def process_mission(zone, mission, state):
    mission_key = f"{zone.id}-{mission.num}"
    if mission_key in state.completed_missions:
        return True

    xp_reward = mission.num * 20
    render_mission(
        zone.name, mission.num, len(zone.missions),
        mission.title, mission.description, mission.example,
        xp_reward,
    )

    code = get_multiline_input(state)
    if code is None:
        return False
    if code == "":
        return True

    stdout, stderr = execute_code(code)
    if stderr:
        console.print(f"[bold red]Error:[/] {stderr}")
        return handle_mission_fail(state, mission, mission_key)

    passed, msg = mission.validation_fn(stdout, stderr)
    if passed:
        state.add_xp(xp_reward)
        state.completed_missions.append(mission_key)
        state.check_mission_achievements(zone.id)
        state.check_zone_complete(zone.id)
        state.check_boss_hunter()
        state.save()
        render_result(state, True, msg, xp_reward)

        if 5 <= zone.id <= 9:
            render_meta_moment(zone.id, mission.num)

        return True
    else:
        console.print(f"[bold red]✗ {msg}[/]")
        console.print(f"[dim]Tu salida: {stdout!r}[/]")
        return handle_mission_fail(state, mission, mission_key)


def handle_mission_fail(state, mission, mission_key):
    choice = console.input("[yellow][H]int [S]kip(-50xp) [R]eintentar [Q]uit: [/]").lower()
    if choice == "h":
        state.hints_used += 1
        if mission.example:
            console.print(f"[cyan]Pista:[/] {mission.example}")
        return None
    elif choice == "s":
        state.missions_skipped += 1
        state.add_xp(-50)
        state.completed_missions.append(mission_key)
        state.save()
        console.print("[red]Misión saltada. -50 XP[/]")
        return True
    elif choice == "q":
        state.save()
        console.print("[yellow]Juego guardado. ¡Hasta luego![/]")
        sys.exit(0)
    return None


def main():
    parser = argparse.ArgumentParser(description="PyQuest — Terminal RPG")
    parser.add_argument("--validate", metavar="ARCHIVO", help="Validar una zona creada por el jugador")
    parser.add_argument("--template", action="store_true", help="Generar template para nueva zona")
    args = parser.parse_args()

    if args.validate:
        errors = validate_zone_file(args.validate)
        if errors:
            console.print("[red]Errores de validación:[/]")
            for e in errors:
                console.print(f"  ✗ {e}")
            sys.exit(1)
        else:
            console.print("[green]✓ Zona válida. Se integrará al juego automáticamente.[/]")
            sys.exit(0)

    if args.template:
        template = generate_template()
        path = "zone_template.py"
        Path(path).write_text(template)
        console.print(f"[green]✓ Template creado: {path}[/]")
        console.print("Edítalo y colócalo en world/zones/")
        sys.exit(0)

    state = GameState.load()
    show_title_screen(state)
    state.save()

    current_act_id = None

    while True:
        zone_info = get_zone(state.unlocked_zones)
        if zone_info is None:
            console.print("[bold green]╔══════════════════════════════════════════╗")
            console.print("[bold green]║  [yellow]¡Has completado todas las zonas![/]       [bold green]║")
            console.print("[bold green]║  [cyan]Eres un verdadero Legend.[/]              [bold green]║")
            console.print("[bold green]╚══════════════════════════════════════════╝")
            show_profile(state)
            break

        zone = ZONE_CLASSES.get(zone_info["id"])
        if zone is None:
            console.print("[bold yellow]╔══════════════════════════════════════════╗")
            console.print("[bold yellow]║  ZONA ∞                                  ║")
            console.print("[bold yellow]║  No hay más zonas predefinidas           ║")
            console.print("[bold yellow]║  Crea la tuya con /crear                 ║")
            console.print("[bold yellow]╚══════════════════════════════════════════╝")
            show_map(state.unlocked_zones)

            if state.unlocked_zones >= 13:
                render_zone_creator_intro()
                choice = console.input("[bold]¿Qué quieres hacer? [C]rear zona  [M]apa  [P]erfil  [S]alir: [/]").lower()
                if choice == "c":
                    handle_command("/crear", state)
                elif choice == "m":
                    show_map(state.unlocked_zones)
                    console.input("[dim]Presiona Enter...[/]")
                elif choice == "p":
                    show_profile(state)
                elif choice == "s":
                    state.save()
                    console.print("[yellow]¡Hasta luego, creador![/]")
                    break
                continue

            console.input("[dim]Presiona Enter para continuar...[/]")
            break

        act = get_act(zone.id)
        if act.id != current_act_id:
            current_act_id = act.id
            render_act_transition(act)

        header = make_header(zone, state, f"Acto {act.id}")
        console.print(header)
        render_story(zone.story_intro)

        for mission in zone.missions:
            while True:
                result = process_mission(zone, mission, state)
                if result is True:
                    break
                elif result is False:
                    return

        state.unlocked_zones += 1
        state.save()
        console.print(f"[bold green]✓ Zona [cyan]{zone.name}[/] completada. ¡A la siguiente![/]")
        show_map(state.unlocked_zones)

        if state.unlocked_zones == 13:
            render_zone_creator_intro()

    if state.unlocked_zones >= 13:
        console.print("[bold yellow]╔══════════════════════════════════════════╗")
        console.print("[bold yellow]║  PyQuest ∞                               ║")
        console.print("[bold yellow]║  El juego ahora crece contigo.           ║")
        console.print("[bold yellow]║  Crea nuevas zonas en world/zones/       ║")
        console.print("[bold yellow]╚══════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
