#!/usr/bin/env python3
"""PyQuest — Terminal RPG para aprender Python.

Uso:
  python main.py                         # Jugar
  python main.py --validate ruta.py      # Validar zona
  python main.py --template              # Generar template
  python main.py --docs [tema]           # Documentación interactiva
  python main.py --playground            # REPL libre
  python main.py --temas [cat]           # Panel de aprendizaje
"""

import sys
import argparse
import time
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.console import console
from engine.renderer import (
    show_title_screen, make_header, render_story,
    render_mission, render_result, show_commands,
    render_meta_moment, render_zone_creator_intro, render_act_rules,
    render_execution_spinner, render_zone_progress, render_zone_complete,
    type_print, IS_TERMUX, COMPACT, show_welcome_new_player, show_quick_tutorial,
    show_return_dashboard, render_orientation_bar, show_daily_tip,
)
from engine.profile import show_profile
from engine.acts import get_act, render_act_transition
from engine.schema import validate_zone_file, generate_template
from engine.validator import validate_code
from engine.state import GameState
from engine.collection import try_collect_object, check_zone_object_unlocked
from engine.menu import TabMenu
from world.map import show_map, get_zone
from world import ZONE_CLASSES


class JumpZone(Exception):
    pass

def show_help():
    show_commands()
    console.input("\n[dim]Presiona Enter para continuar...[/]")


def cmd_docs(args: str = ""):
    from engine.pyhelp import show_docs
    show_docs(args)


def cmd_playground():
    from engine.pyhelp import show_playground
    show_playground()


def cmd_temas(args: str = ""):
    from engine.panel import show_panel
    show_panel(args)


def cmd_git_pull():
    console.print("[yellow]📦 Buscando actualizaciones desde Git...[/]")
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True, text=True, timeout=30,
            cwd=Path(__file__).resolve().parent,
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if "Already up to date" in output or "Ya está actualizado" in output:
                console.print("[green]✓ PyQuest ya está actualizado[/]")
            else:
                console.print(f"[green]✓ Actualizado:[/]\n{output}")
        else:
            console.print(f"[red]Error al actualizar:\n{result.stderr}[/]")
    except FileNotFoundError:
        console.print("[red]❌ Git no está instalado. Instálalo con: pkg install git[/]")
    except subprocess.TimeoutExpired:
        console.print("[red]❌ Tiempo de espera agotado[/]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
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
    elif cmd.startswith("/docs"):
        parts = cmd.split(maxsplit=1)
        args = parts[1] if len(parts) > 1 else ""
        cmd_docs(args)
        return True
    elif cmd.startswith("/temas"):
        parts = cmd.split(maxsplit=1)
        args = parts[1] if len(parts) > 1 else ""
        cmd_temas(args)
        return True
    elif cmd == "/playground":
        cmd_playground()
        return True
    elif cmd.startswith("/git"):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1 and parts[1] == "pull":
            cmd_git_pull()
        else:
            console.print("[yellow]Usa: /git pull[/]")
            console.input("\n[dim]Presiona Enter...[/]")
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
    elif cmd.startswith("/saltar"):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].isdigit():
            console.print("[red]Usa: /saltar <numero>[/]")
            console.input("\n[dim]Presiona Enter...[/]")
            return True
        target_zone = int(parts[1])
        if target_zone < 1 or target_zone > 15:
            console.print("[red]Zona inválida (1-15)[/]")
            console.input("\n[dim]Presiona Enter...[/]")
            return True
        state.unlocked_zones = target_zone
        state.save()
        console.print(f"[green]Saltando a la Zona {target_zone}...[/]")
        import time; time.sleep(0.5)
        raise JumpZone()
    elif cmd == "/menu":
        show_profile(state)
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
    from ui.editor import mini_editor
    text = mini_editor(hints_left=hints_left)
    if text is None:
        return None
    if text.startswith("/"):
        if handle_command(text, state):
            return ""
        return ""
    return text


def process_mission(zone, mission, state, act):
    mission_key = f"{zone.id}-{mission.num}"
    if mission_key in state.completed_missions:
        return True

    xp_reward = int(mission.xp_reward * act.xp_multiplier)
    max_hints = act.max_hints_per_mission

    # ── ORIENTACIÓN PERSISTENTE ──
    render_orientation_bar(
        zone.id, len(zone.missions),
        mission.num, len(zone.missions),
        state, max_hints if max_hints >= 0 else -1,
    )
    
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

    # ── PANEL DE FALLA CONTEXTUAL ──
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    
    fail_panel = Text()
    fail_panel.append("✗ Tu código no pasó las pruebas\n\n", style="bold red")
    fail_panel.append(f"¿Qué puedes hacer?\n\n", style="white")
    fail_panel.append("  [yellow][R][/] Reintentar  — vuelve a escribir tu solución\n", style="white")
    fail_panel.append("  [cyan][H][/] Pedir pista  — una ayuda sin spoilers\n", style="white")  
    fail_panel.append("  [blue][D][/] Ver docs     — documentación de Python\n", style="white")
    fail_panel.append("  [dim][S][/] Saltar       — avanza (pierdes 50 XP)\n", style="white")
    fail_panel.append("  [dim][Q][/] Salir        — guardar y cerrar\n", style="white")
    
    console.print(Panel(
        fail_panel,
        title="🔧 Taller de Debug",
        border_style="red",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    
    has_hints = bool(mission.hints)
    hints_in_zone = state.hints_used_in_zone.get(str(state.unlocked_zones), 0)
    can_hint = act.max_hints_per_mission == -1 or hints_in_zone < act.max_hints_per_mission

    choice = console.input("[bold]Tu elección (R/H/D/S/Q): [/]").lower()
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
    elif choice == "d":
        from engine.pyhelp import show_docs
        show_docs()
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
    parser.add_argument("--docs", nargs="?", const="", metavar="TEMA", help="Abrir documentación interactiva")
    parser.add_argument("--playground", action="store_true", help="Abrir REPL libre")
    parser.add_argument("--temas", nargs="?", const="", metavar="CAT", help="Abrir panel de aprendizaje")
    args = parser.parse_args()

    if args.temas is not None:
        from engine.panel import show_panel
        show_panel(args.temas)
        sys.exit(0)

    if args.docs is not None:
        from engine.pyhelp import show_docs
        show_docs(args.docs)
        sys.exit(0)

    if args.playground:
        from engine.pyhelp import show_playground
        show_playground()
        sys.exit(0)

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
    
    # ── NUEVO JUGADOR: Onboarding para primera vez ──
    if not state.completed_missions:        # ← primera vez
        show_welcome_new_player()
        show_quick_tutorial()               # ← tutorial de 2 pasos
        state.is_tutorial_done = True
    
    state.save()

    current_act_id = None
    shown_dashboard = False

    while True:
        try:
            # ── JUGADOR REGRESANDO: Dashboard de retorno ──
            if state.total_missions > 0 and not shown_dashboard:
                choice = show_return_dashboard(state)
                if choice.startswith("/"):
                    handle_command(choice, state)
                    continue
                elif choice == "j":
                    zone_str = console.input("[bold yellow]¿A qué zona quieres ir? (1-15): [/]")
                    handle_command(f"/saltar {zone_str}", state)
                    continue
                elif choice == "m":
                    show_map(state.unlocked_zones)
                    console.input("[dim]Presiona Enter...[/]")
                    continue
                elif choice == "p":
                    show_profile(state)
                    continue
                elif choice == "d":
                    cmd_docs()
                    continue
                elif choice == "s":
                    state.save()
                    console.print("\n[bold yellow]Juego guardado. ¡Hasta luego, dev![/]")
                    sys.exit(0)
                shown_dashboard = True
            
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
                    choice = console.input("[bold]¿Qué quieres hacer? [C]rear  [D]ocs  [T]emas  [M]apa  [J]ugar otra zona  [P]erfil  [S]alir: [/]").lower()
                    if choice.startswith("/"):
                        handle_command(choice, state)
                    elif choice == "c":
                        handle_command("/crear", state)
                    elif choice == "d":
                        cmd_docs()
                    elif choice == "t":
                        cmd_temas()
                    elif choice == "m":
                        show_map(state.unlocked_zones)
                        console.input("[dim]Presiona Enter...[/]")
                    elif choice == "j":
                        zone_str = console.input("[bold yellow]¿A qué zona quieres ir? (1-15): [/]")
                        handle_command(f"/saltar {zone_str}", state)
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

            obj_name = try_collect_object(zone.id, state.completed_missions, state.collected_objects)
            if obj_name:
                console.print(f"[bold cyan]💠 ¡Has recolectado: {obj_name}![/]")
                console.print("[dim]Revisa tu colección en el perfil.[/]")

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

            if state.unlocked_zones == 16:
                render_zone_creator_intro()
                
        except JumpZone:
            shown_dashboard = True
            console.clear()
            continue

    if state.unlocked_zones >= 16:
        console.print("[bold yellow]╔══════════════════════════════════════════╗")
        console.print("[bold yellow]║  PyQuest ∞                               ║")
        console.print("[bold yellow]║  El juego ahora crece contigo.           ║")
        console.print("[bold yellow]║  Crea nuevas zonas en world/zones/       ║")
        console.print("[bold yellow]╚══════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
