"""
Modello di una regola matematica applicabile.

Una ``Rule`` può essere definita in due modalità:

1. **Pattern-based**: con un pattern SymPy e un replacement. Usa
   ``expr.match(pattern)`` per riconoscere quando si applica.
   Adatta a pattern molto specifici.

2. **Function-based**: con una funzione ``try_apply(expr) -> expr | None``.
   La funzione analizza l'espressione e restituisce la trasformazione
   o ``None``. Adatta a pattern generici dove il matching di SymPy
   è troppo aggressivo o impreciso.

Il resto del codice (motore, ``make_step``) usa ``Rule`` in modo
uniforme, indipendentemente dalla modalità.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import sympy

from openalpha.core.step import Step


@dataclass(frozen=True)
class Rule:
    """Una regola matematica applicabile.

    Attributi:
        name: identificatore univoco.
        description: descrizione generica della regola.
        pattern: pattern SymPy (solo per modalità pattern-based).
        replacement: funzione di sostituzione (solo per pattern-based).
        condition: funzione opzionale di filtro (solo per pattern-based).
        try_apply: funzione di applicazione (solo per function-based).

    Una Rule è o pattern-based o function-based. Mai entrambe.
    """

    name: str
    description: str
    pattern: sympy.Expr | None = None
    replacement: Callable[[dict], sympy.Expr] | None = None
    condition: Callable[[dict], bool] | None = None
    try_apply: Callable[[sympy.Expr], sympy.Expr | None] | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("'name' non può essere vuoto")
        if not self.description:
            raise ValueError("'description' non può essere vuota")

        is_pattern = self.pattern is not None or self.replacement is not None
        is_function = self.try_apply is not None

        if is_pattern and is_function:
            raise ValueError(
                "Una Rule non può essere contemporaneamente pattern-based "
                "e function-based"
            )
        if not is_pattern and not is_function:
            raise ValueError(
                "Una Rule deve essere pattern-based o function-based"
            )
        if is_pattern:
            if self.pattern is None:
                raise ValueError("pattern-based richiede 'pattern'")
            if self.replacement is None:
                raise ValueError("pattern-based richiede 'replacement'")

    @classmethod
    def from_pattern(
        cls,
        name: str,
        description: str,
        pattern: sympy.Expr,
        replacement: Callable[[dict], sympy.Expr],
        condition: Callable[[dict], bool] | None = None,
    ) -> "Rule":
        """Costruisce una Rule pattern-based."""
        return cls(
            name=name,
            description=description,
            pattern=pattern,
            replacement=replacement,
            condition=condition,
        )

    @classmethod
    def from_function(
        cls,
        name: str,
        description: str,
        try_apply: Callable[[sympy.Expr], sympy.Expr | None],
    ) -> "Rule":
        """Costruisce una Rule function-based."""
        return cls(
            name=name,
            description=description,
            try_apply=try_apply,
        )


def apply_rule(rule: Rule, expr: sympy.Expr) -> sympy.Expr | None:
    """Applica una regola a un'espressione.

    Args:
        rule: la regola da applicare.
        expr: l'espressione su cui applicarla.

    Returns:
        L'espressione trasformata se la regola si applica, ``None``
        altrimenti.
    """
    # Modalità function-based
    if rule.try_apply is not None:
        try:
            return rule.try_apply(expr)
        except Exception:
            # Se la funzione solleva, la regola non si applica.
            return None

    # Modalità pattern-based
    match = expr.match(rule.pattern)  # type: ignore[arg-type]
    if match is None:
        return None

    expected_wilds = rule.pattern.atoms(sympy.Wild)  # type: ignore[union-attr]
    if not expected_wilds.issubset(match.keys()):
        return None

    if rule.condition is not None and not rule.condition(match):
        return None

    return rule.replacement(match)  # type: ignore[misc]


def make_step(
    rule: Rule,
    before_expr: sympy.Expr,
    description: str,
    conditions: list[str] | None = None,
) -> Step | None:
    """Costruisce uno ``Step`` verificato applicando una regola."""
    after_expr = apply_rule(rule, before_expr)
    if after_expr is None:
        return None

    before_str = str(before_expr)
    after_str = str(after_expr)

    if before_str == after_str:
        return None

    return Step(
        before=before_str,
        after=after_str,
        rule_name=rule.name,
        description=description,
        conditions=list(conditions) if conditions else [],
    )