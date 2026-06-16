#!/usr/bin/env python3
"""PyQuest — Terminal RPG para aprender Python.

Uso:
  python main.py                         # Jugar
  python main.py --validate ruta.py      # Validar zona
  python main.py --template              # Generar template
"""

import sys
import argparse
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.console import console
from engine.renderer import (
    show_title_screen, make_header, render_story,
    render_mission, render_result, show_commands,
    render_meta_moment, render_zone_creator_intro, render_act_rules,
    render_execution_spinner, render_zone_progress, render_zone_complete,
    type_print,
)
from engine.profile import show_profile
from engine.acts import get_act, render_act_transition
from engine.schema import validate_zone_file, generate_template
from engine.validator import validate_code
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
    elif cmd.startswith("/acto"):
        act = get_act(state.unlocked_zones)
        render_act_rules(act)
        console.input("\n[dim]Presiona Enter para continuar...[/]")
        return True
    elif cmd == "/crear":
        template = generate_template(state.player_name)
        path = Path("world/zones") / f"zone_13_{state.player_name.lower()}_zone.py"
        path.write_text(template)
        console.print(f"[green]✓ Template creado: {path}[/]")
        console.print("[dim]Edítalo y el juego lo descubrirá automáticamente.[/]")
        state.add_achievement("creador")
        state.save()
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


def get_multiline_input(state: GameState, hints_left: int = -1) -> str | None:
    hint_status = ""
    if hints_left >= 0:
        hint_status = f"  💡{hints_left} hints restantes"
    console.print(f"[dim](Escribe código o /comando  •  Ctrl+D enviar  •  Ctrl+C salir{hint_status})[/]")
    first_line = console.input("[bold green]  >>> [/]")
    if first_line.startswith("/"):
        if handle_command(first_line, state):
            return ""
        return ""

    lines = [first_line]
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


def process_mission(zone, mission, state, act):
    mission_key = f"{zone.id}-{mission.num}"
    if mission_key in state.completed_missions:
        return True

    xp_reward = int(mission.xp_reward * act.xp_multiplier)
    max_hints = act.max_hints_per_mission

    render_mission(
        zone.name, mission.num, len(zone.missions),
        mission.title, mission.description,
        mission.code_template if act.code_template_required or mission.code_template else None,
        xp_reward,
        hints_left=max_hints if max_hints >= 0 else -1,
        act=act,
    )

    code = get_multiline_input(state, max_hints if max_hints >= 0 else -1)
    if code is None:
        return False
    if code == "":
        return True

    t0 = time.time()
    old_level = state.level

    with render_execution_spinner("code"):
        all_passed = True
        last_msg = ""
        for tc in mission.test_cases:
            passed, msg, _ = validate_code(code, mission.execution_mode, [tc])
            if not passed:
                all_passed = False
                last_msg = msg
                break

    elapsed = time.time() - t0
    state.missions_time[mission_key] = elapsed

    if all_passed:
        state.add_xp(xp_reward)
        state.add_xp_to_zone(zone.id, xp_reward)
        state.completed_missions.append(mission_key)
        state.check_mission_achievements(zone.id)
        state.check_zone_complete(zone.id)
        state.check_boss_hunter()
        state.save()
        render_result(state, True, msg or "✓ Misión completada", xp_reward, old_level)

        if 5 <= zone.id <= 9:
            render_meta_moment(zone.id, mission.num)
        return True
    else:
        state.missions_failed += 1
        console.print(f"\n[bold red]✗ {last_msg}[/]")
        return handle_mission_fail(state, mission, mission_key, act)


def handle_mission_fail(state, mission, mission_key, act):
    if not act.allow_skip_with_penalty:
        console.print("[yellow]En este acto no puedes saltar misiones. ¡Sigue intentando![/]")
        return None

    has_hints = bool(mission.hints)
    hints_in_zone = state.hints_used_in_zone.get(str(state.unlocked_zones), 0)
    can_hint = act.max_hints_per_mission == -1 or hints_in_zone < act.max_hints_per_mission

    options = "[R]eintentar"
    if has_hints and can_hint and act.max_hints_per_mission != 0:
        options += " [H]int"
    if act.allow_skip_with_penalty:
        options += " [S]kip(-50xp)"
    options += " [Q]uit"

    choice = console.input(f"[yellow]{options}: [/]").lower()
    if choice == "h" and has_hints and can_hint:
        state.hints_used += 1
        key = str(state.unlocked_zones)
        state.hints_used_in_zone[key] = state.hints_used_in_zone.get(key, 0) + 1
        hint_idx = state.hints_used_in_zone[key] - 1
        if hint_idx < len(mission.hints):
            console.print(f"[cyan]Pista {hint_idx + 1}:[/] {mission.hints[hint_idx]}")
        elif mission.code_template:
            console.print(f"[cyan]Código base:[/] {mission.code_template}")
        return None
    elif choice == "s" and act.allow_skip_with_penalty:
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
    parser.add_argument("--validate", metavar="ARCHIVO", help="Validar una zona del jugador")
    parser.add_argument("--template", action="store_true", help="Generar template de zona")
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
        Path("zone_template.py").write_text(template)
        console.print(f"[green]✓ Template creado: zone_template.py[/]")
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
            console.print("[yellow]Zona no encontrada.[/]")
            console.input("[dim]Presiona Enter...[/]")
            break

        act = get_act(zone.id)
        if act.id != current_act_id:
            current_act_id = act.id
            render_act_transition(act)
            if zone.id > 1:
                state.check_act_completion(get_act(zone.id - 1).id)

        header = make_header(zone, state, act)
        console.print(header)
        render_act_rules(act)
        render_zone_progress(0, len(zone.missions), zone.name)
        render_story(zone.story_intro)

        zone_stats = {"xp": 0, "hints": 0, "failed": 0, "completed": 0, "skipped": 0}
        t_zone_start = time.time()

        for mission in zone.missions:
            while True:
                result = process_mission(zone, mission, state, act)
                if result is True:
                    zone_stats["completed"] += 1
                    zone_stats["xp"] += int(mission.xp_reward * act.xp_multiplier)
                    break
                elif result is False:
                    return

        elapsed = time.time() - t_zone_start

        state.unlocked_zones += 1
        state.save()
        render_zone_complete(
            zone.name, zone.id,
            len(zone.missions),
            zone_stats["completed"],
            zone_stats["skipped"],
            zone_stats["failed"],
            zone_stats["hints"],
            zone_stats["xp"],
            elapsed,
        )
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
