"""
Libreria delle regole matematiche concrete di OpenAlpha.

Le regole sono di due tipi:

- **Pattern-based**: usano il matching di SymPy. Adatte a pattern
  specifici dove il match è affidabile.
- **Function-based**: analizzano esplicitamente l'espressione. Adatte
  a pattern generici dove il matching di SymPy è troppo aggressivo.
"""

from __future__ import annotations

import sympy

from openalpha.explanations.rules import Rule


def _square_of_binomial_rule() -> Rule:
    """(a + b)**2 → a**2 + 2*a*b + b**2."""
    a = sympy.Wild("a")
    b = sympy.Wild("b")
    return Rule.from_pattern(
        name="square_of_binomial",
        description="Quadrato del binomio: (a + b)**2 = a**2 + 2*a*b + b**2",
        pattern=(a + b) ** 2,
        replacement=lambda m: m[a] ** 2 + 2 * m[a] * m[b] + m[b] ** 2,
    )


def _difference_of_squares_rule() -> Rule:
    """a**2 - b**2 → (a - b)*(a + b).

    Regola **function-based**: analizza esplicitamente l'Add per
    trovare due termini con esponente 2 e segni opposti. Non usa
    pattern matching, perché ``a**2 - b**2`` come pattern matcha
    anche espressioni degeneri (es. ``x + 1 = (sqrt(x))**2 - (I)**2``).
    """

    def _try_apply(expr: sympy.Expr) -> sympy.Expr | None:
        if not expr.is_Add:
            return None

        # Separa i termini in positivi e negativi.
        positives = []
        negatives = []
        for term in expr.args:
            coeff, rest = term.as_coeff_Mul()
            if coeff.is_negative:
                negatives.append(-term)  # rendiamo positivo
            else:
                positives.append(term)

        # Cerca una coppia (positivo, negativo) di quadrati.
        for pos in positives:
            a = _extract_square_base(pos)
            if a is None:
                continue
            for neg in negatives:
                b = _extract_square_base(neg)
                if b is None:
                    continue
                # Verifica: a e b non contengono sqrt o I,
                # e almeno uno contiene una variabile.
                if _has_bad_symbols(a) or _has_bad_symbols(b):
                    continue
                if not (a.free_symbols or b.free_symbols):
                    continue
                return (a - b) * (a + b)
        return None

    return Rule.from_function(
        name="difference_of_squares",
        description="Differenza di quadrati: a**2 - b**2 = (a - b)*(a + b)",
        try_apply=_try_apply,
    )


def _extract_square_base(term: sympy.Expr) -> sympy.Expr | None:
    """Se ``term`` è ``base**2``, restituisce ``base``. Altrimenti ``None``.

    Tratta anche le costanti positive come quadrati: 1 → 1, 4 → 2, ecc.
    Necessario per gestire casi come ``x**2 - 1``, dove ``1`` è il
    quadrato di ``1``.
    """
    if isinstance(term, sympy.Pow) and term.exp == 2:
        return term.base
    # Costanti positive: verifica se hanno radice intera.
    if term.is_Number and term.is_positive:
        root = sympy.sqrt(term)
        if root.is_integer:
            return root
    return None

def _has_bad_symbols(expr: sympy.Expr) -> bool:
    """True se l'espressione contiene sqrt o I."""
    return bool(expr.has(sympy.sqrt) or expr.has(sympy.I))


def _common_factor_rule() -> Rule:
    """a*b + a*c → a*(b + c)."""
    a = sympy.Wild("a")
    b = sympy.Wild("b")
    c = sympy.Wild("c")

    def _condition(match: dict) -> bool:
        # Almeno uno tra b e c deve essere non banale.
        b_val = match[b]
        c_val = match[c]
        if b_val == 0 or c_val == 0:
            return False
        return True

    return Rule.from_pattern(
        name="common_factor",
        description="Raccoglimento a fattor comune: a*b + a*c = a*(b + c)",
        pattern=a * b + a * c,
        replacement=lambda m: m[a] * (m[b] + m[c]),
        condition=_condition,
    )


def _cancel_common_factor_rule() -> Rule:
    """(a*b) / (a*c) → b / c."""
    a = sympy.Wild("a", exclude=[0])
    b = sympy.Wild("b")
    c = sympy.Wild("c", exclude=[0])
    return Rule.from_pattern(
        name="cancel_common_factor",
        description="Cancellazione di fattore comune: (a*b) / (a*c) = b / c",
        pattern=(a * b) / (a * c),
        replacement=lambda m: m[b] / m[c],
    )


def _power_of_power_rule() -> Rule:
    """(a**b)**c → a**(b*c)."""
    a = sympy.Wild("a")
    b = sympy.Wild("b")
    c = sympy.Wild("c")
    return Rule.from_pattern(
        name="power_of_power",
        description="Potenza di potenza: (a**b)**c = a**(b*c)",
        pattern=(a**b) ** c,
        replacement=lambda m: m[a] ** (m[b] * m[c]),
    )


def default_rules() -> list[Rule]:
    """Restituisce la lista delle regole di default."""
    return [
        _square_of_binomial_rule(),
        _difference_of_squares_rule(),
        _common_factor_rule(),
        _cancel_common_factor_rule(),
        _power_of_power_rule(),
    ]