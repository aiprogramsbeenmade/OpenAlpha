"""
Motore delle spiegazioni: applica le regole e produce gli Step.

Dato un'espressione SymPy, il motore:

1. Applica le regole in sequenza, in modo esaustivo ma controllato.
2. Per ogni applicazione, produce uno ``Step`` verificato.
3. Si ferma quando nessuna regola si applica, o al limite di passi.
4. Restituisce la lista di ``Step`` e il risultato finale.

Il motore NON semplifica automaticamente con ``sympy.simplify``:
quello è compito del chiamante. Il motore applica solo le regole
dichiarate, e produce solo passi verificati.

## Stati della spiegazione

- ``complete``: il motore ha applicato almeno una regola e si è
  fermato perché nessuna regola del set corrente si applicava più.
  La spiegazione è completa **rispetto alle regole disponibili**,
  non in senso assoluto.
- ``partial``: il motore ha raggiunto il limite di passi senza
  fermarsi per esaurimento delle regole.
- ``unavailable``: il motore non ha applicato nessuna regola.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy

from openalpha.core.step import Step
from openalpha.explanations.rules import Rule, apply_rule, make_step
from openalpha.explanations.rules_library import default_rules

# Limite di sicurezza: massimo numero di passi per una spiegazione.
# Evita loop infiniti se una regola si riapplica ciclicamente.
_MAX_STEPS = 20


@dataclass
class ExplanationResult:
    """Risultato del motore delle spiegazioni.

    Attributi:
        final_expr: espressione finale dopo l'applicazione delle regole.
        steps: lista di ``Step`` verificati.
        complete: ``True`` se la spiegazione è completa rispetto alle
            regole disponibili; ``False`` altrimenti.
        status: uno tra ``"complete"``, ``"partial"``, ``"unavailable"``.
        message: messaggio esplicativo per l'utente.
    """

    final_expr: sympy.Expr
    steps: list[Step]
    complete: bool
    status: str
    message: str


def _apply_rule_anywhere(
    rule: Rule, expr: sympy.Expr
) -> tuple[sympy.Expr | None, str | None]:
    """Applica una regola a un sottoalbero qualsiasi di ``expr``.

    Esplora l'albero bottom-up con ``expr.args``, applicando la regola
    a ogni nodo. Si ferma alla prima applicazione riuscita.

    Non usa ``sympy.replace``: quest'ultimo ri-semplifica il risultato
    e scarta le sostituzioni che SymPy considera equivalenti
    all'originale.

    Restituisce una tupla ``(nuova_expr, contesto)``:
    - ``nuova_expr`` è l'espressione trasformata, o ``None`` se la
      regola non si applica da nessuna parte;
    - ``contesto`` è una stringa che descrive il sottoalbero
      trasformato, o ``None``.
    """
    # Prova prima alla radice: il match è più economico.
    transformed_root = apply_rule(rule, expr)
    if transformed_root is not None and str(transformed_root) != str(expr):
        return transformed_root, str(expr)

    # Esplora i figli bottom-up.
    if not expr.args:
        return None, None

    new_args = []
    changed = False
    context = None
    for arg in expr.args:
        if changed:
            new_args.append(arg)
            continue
        transformed_arg, ctx = _apply_rule_anywhere(rule, arg)
        if transformed_arg is not None:
            new_args.append(transformed_arg)
            changed = True
            context = ctx
        else:
            new_args.append(arg)

    if not changed:
        return None, None

    # Ricostruisce il nodo con i nuovi args.
    try:
        new_expr = expr.func(*new_args)
    except Exception:
        return None, None
    return new_expr, context


def explain(
    expr: sympy.Expr,
    rules: list[Rule] | None = None,
) -> ExplanationResult:
    """Applica le regole in sequenza, producendo Step verificati.

    Args:
        expr: espressione SymPy da spiegare.
        rules: lista di regole da usare. Se ``None``, usa
            ``default_rules()``.

    Returns:
        Un ``ExplanationResult`` con i passi applicati e il risultato
        finale.
    """
    if rules is None:
        rules = default_rules()

    steps: list[Step] = []
    current = expr
    reached_limit = True

    for _ in range(_MAX_STEPS):
        progress = False
        for rule in rules:
            new_expr, context = _apply_rule_anywhere(rule, current)
            if new_expr is None:
                continue
            description = (
                f"{rule.description} ({context})" if context else rule.description
            )
            step = make_step(rule, current, description=description)
            if step is None:
                continue
            steps.append(step)
            current = new_expr
            progress = True
            break
        if not progress:
            reached_limit = False
            break

    if not steps:
        return ExplanationResult(
            final_expr=expr,
            steps=[],
            complete=False,
            status="unavailable",
            message=(
                "spiegazione non disponibile: nessun procedimento "
                "verificato per questa espressione"
            ),
        )

    if reached_limit:
        return ExplanationResult(
            final_expr=current,
            steps=steps,
            complete=False,
            status="partial",
            message=(
                f"spiegazione parziale: raggiunto il limite di "
                f"{_MAX_STEPS} passi"
            ),
        )

    return ExplanationResult(
        final_expr=current,
        steps=steps,
        complete=True,
        status="complete",
        message="spiegazione completa rispetto alle regole disponibili",
    )