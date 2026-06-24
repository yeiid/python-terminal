from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align
from rich.console import Console
from ui.responsive import responsive


console = Console(highlight=False)


def format_code_output(code: str, indent_level: int = 0) -> str:
    indent = "  " * indent_level
    return "\n".join(f"{indent}{line}" for line in code.split("\n"))


def format_comparison(expected: str, received: str) -> str:
    result = []
    exp_lines = expected.split("\n")
    rec_lines = received.split("\n")
    max_len = max(len(exp_lines), len(rec_lines), 1)
    for i in range(max_len):
        e = exp_lines[i] if i < len(exp_lines) else ""
        r = rec_lines[i] if i < len(rec_lines) else ""
        if e == r:
            result.append(f"  ✓  {e}")
        else:
            e_repr = repr(e) if e != e.strip() else e
            r_repr = repr(r) if r != r.strip() else r
            result.append(f"  ✗  esperado: {e_repr}")
            result.append(f"     recibido: {r_repr}")
    return "\n".join(result)


from rich.table import Table

def show_expected_vs_received(expected: str, received: str, case_num: int = 0):
    title_suffix = f" (Caso {case_num})" if case_num else ""
    
    if responsive.compact:
        console.print(f"[bold red]🔍 Análisis de Resultados{title_suffix}[/]")
        exp_panel = Panel(Text(expected if expected else "(vacío)", style="green"), title="Esperado", border_style="green", box=box.SIMPLE)
        rec_panel = Panel(Text(received if received else "(vacío)", style="red"), title="Recibido", border_style="red", box=box.SIMPLE)
        console.print(exp_panel)
        console.print(rec_panel)
    else:
        table = Table(
            title=f"🔍 Análisis de Resultados{title_suffix}", 
            box=box.ROUNDED, 
            border_style="red",
            width=responsive.max_content_width if responsive.max_content_width else None,
            show_lines=True
        )
        table.add_column("Lo que se esperaba", style="green", ratio=1)
        table.add_column("Lo que devolvió tu código", style="red", ratio=1)
        
        exp_lines = (expected or "").splitlines()
        rec_lines = (received or "").splitlines()
        
        max_len = max(len(exp_lines), len(rec_lines))
        for i in range(max_len):
            e = exp_lines[i] if i < len(exp_lines) else ""
            r = rec_lines[i] if i < len(rec_lines) else ""
            
            e_text = Text(e) if e else Text("(vacío)", style="dim")
            r_text = Text(r) if r else Text("(vacío)", style="dim")
            
            if e == r:
                table.add_row(e_text, r_text, style="dim")
            else:
                table.add_row(e_text, r_text)
                
        console.print(table)
        
    if expected.strip() == received.strip() and expected != received:
        console.print("[yellow]💡 Pista: Tu resultado parece correcto, pero tiene espacios o saltos de línea extra.[/]")
        console.print()

def show_diff(expected: str, received: str, case_num: int = 0):
    show_expected_vs_received(expected, received, case_num)
