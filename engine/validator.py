def validate(
    stdout: str,
    expected: str | None = None,
    test_cases: list[tuple[str, str]] | None = None,
) -> tuple[bool, str]:
    """Valida la salida del código contra lo esperado.
    Retorna (pasó, mensaje)."""
    if test_cases:
        for i, (inp, outp) in enumerate(test_cases, 1):
            if inp.strip() != outp.strip():
                return False, f"Caso {i} falló.\n  Esperado: {outp!r}\n  Recibido:  {inp!r}"
        return True, "✓ Todos los casos pasaron."

    if expected is not None:
        if stdout.strip() == expected.strip():
            return True, "✓ Correcto."
        return False, f"  Esperado: {expected!r}\n  Recibido:  {stdout!r}"

    return True, "✓ Ejecutado sin errores."
