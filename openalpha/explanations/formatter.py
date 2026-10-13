"""
Formattazione dei passi di un procedimento per la presentazione.

Trasforma oggetti ``Step`` in testo leggibile. Il formatter è
**separato** dal ``Result`` e dal motore: è una funzione di
presentazione, specifica del contesto.

CLI e GUI useranno formatter diversi (uno compatto, l'altro ricco),
ma entrambi lavorano sugli stessi ``Step``.
"""

from __future__ import annotations

from openalpha.core.step import Step


def format_step(step: Step, number: int | None = None) -> str:
    """Formatta un singolo passo.

    Args:
        step: il passo da formattare.
        number: numero del passo, se si vuole numerarlo. ``None``
            per non numerare.

    Returns:
        Una stringa multilinea, senza indentazione finale.
    """
    prefix = f"Passo {number}: " if number is not None else ""
    lines = [
        f"{prefix}{step.description}",
        f"  {step.before}",
        f"  → {step.after}",
    ]
    if step.conditions:
        lines.append(f"  condizioni: {', '.join(step.conditions)}")
    return "\n".join(lines)


def format_steps(steps: list[Step], *, numbered: bool = True) -> str:
    """Formatta una lista di passi.

    Args:
        steps: i passi da formattare.
        numbered: se ``True``, numera i passi partendo da 1.

    Returns:
        Una stringa con i passi separati da una riga vuota. Stringa
        vuota se la lista è vuota.
    """
    if not steps:
        return ""
    parts = []
    for i, step in enumerate(steps, start=1):
        number = i if numbered else None
        parts.append(format_step(step, number=number))
    return "\n\n".join(parts)