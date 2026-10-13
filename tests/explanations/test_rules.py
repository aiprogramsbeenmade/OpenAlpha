"""
Test del modello ``Rule``, di ``apply_rule`` e di ``make_step``.

Verificano: costruzione di regole valide, applicazione corretta,
mancata applicazione (None), costruzione di Step verificati,
rifiuto di Step quando la regola non cambia nulla.
"""

from __future__ import annotations

import sympy
import pytest

from openalpha.explanations.rules import Rule, apply_rule, make_step


# ---------------------------------------------------------------------------
# Regole di test (usate solo qui)
# ---------------------------------------------------------------------------

def _square_of_binomial_rule() -> Rule:
    """(a + b)**2 → a**2 + 2*a*b + b**2.

    Nota: pattern e replacement usano ``Wild``, non ``Symbol``.
    Con ``Symbol``, il pattern cercherebbe letteralmente i simboli
    ``a`` e ``b``, e non matcherebbe mai un input come ``(x + y)**2``.
    """
    a = sympy.Wild("a")
    b = sympy.Wild("b")
    return Rule(
        name="square_of_binomial",
        description="Quadrato del binomio",
        pattern=(a + b) ** 2,
        replacement=lambda m: m[a] ** 2 + 2 * m[a] * m[b] + m[b] ** 2,
    )


# ---------------------------------------------------------------------------
# Costruzione di Rule
# ---------------------------------------------------------------------------

def test_rule_valida():
    rule = _square_of_binomial_rule()
    assert rule.name == "square_of_binomial"
    assert rule.description == "Quadrato del binomio"


def test_rule_name_vuoto_rifiutato():
    with pytest.raises(ValueError, match="name"):
        Rule.from_function(
            name="",
            description="d",
            try_apply=lambda e: None,
        )


def test_rule_description_vuota_rifiutata():
    with pytest.raises(ValueError, match="description"):
        Rule.from_function(
            name="r",
            description="",
            try_apply=lambda e: None,
        )

# ---------------------------------------------------------------------------
# apply_rule
# ---------------------------------------------------------------------------

def test_apply_rule_si_applica():
    rule = _square_of_binomial_rule()
    x, y = sympy.symbols("x y")
    result = apply_rule(rule, (x + y) ** 2)
    assert result is not None
    assert sympy.simplify(result - (x**2 + 2 * x * y + y**2)) == 0


def test_apply_rule_non_si_applica():
    rule = _square_of_binomial_rule()
    x = sympy.Symbol("x")
    # sin(x) non è (a + b)**2: nessun esponente 2.
    # Nota: non usiamo x**2 perché SymPy lo scompone in (x + 0)**2
    # con Wild b = 0, quindi il pattern matcha per un caso degenere.
    result = apply_rule(rule, sympy.sin(x))
    assert result is None


# ---------------------------------------------------------------------------
# make_step
# ---------------------------------------------------------------------------

def test_make_step_costruisce_step():
    rule = _square_of_binomial_rule()
    x, y = sympy.symbols("x y")
    step = make_step(
        rule,
        (x + y) ** 2,
        description="Applico il quadrato del binomio a (x + y)**2",
    )
    assert step is not None
    assert step.before == str((x + y) ** 2)
    assert step.rule_name == "square_of_binomial"
    assert step.description.startswith("Applico")
    # after è calcolato dalla regola, non scritto a mano.
    atteso = str(x**2 + 2 * x * y + y**2)
    assert sympy.simplify(sympy.sympify(step.after) - sympy.sympify(atteso)) == 0


def test_make_step_restituisce_none_se_regola_non_si_applica():
    rule = _square_of_binomial_rule()
    x = sympy.Symbol("x")
    step = make_step(rule, sympy.sin(x), description="...")
    assert step is None


def test_make_step_con_condizioni():
    rule = _square_of_binomial_rule()
    x, y = sympy.symbols("x y")
    step = make_step(
        rule,
        (x + y) ** 2,
        description="...",
        conditions=["x > 0"],
    )
    assert step is not None
    assert step.conditions == ["x > 0"]


def test_make_step_condizioni_default_vuote():
    rule = _square_of_binomial_rule()
    x, y = sympy.symbols("x y")
    step = make_step(rule, (x + y) ** 2, description="...")
    assert step is not None
    assert step.conditions == []


def test_make_step_restituisce_none_se_non_cambia_nulla():
    """Una regola che non cambia l'espressione non produce uno Step."""
    w = sympy.Wild("w")
    # Regola identità: pattern Wild, replacement Wild. Non cambia nulla.
    identity_rule = Rule(
        name="identity",
        description="Identità",
        pattern=w,
        replacement=lambda m: m[w],
    )
    step = make_step(identity_rule, sympy.Symbol("y"), description="...")
    assert step is None


def test_make_step_immutabile():
    """Lo Step prodotto è immutabile."""
    rule = _square_of_binomial_rule()
    x, y = sympy.symbols("x y")
    step = make_step(rule, (x + y) ** 2, description="...")
    assert step is not None
    with pytest.raises(Exception):
        step.before = "nuovo"  # type: ignore[misc]

def test_rule_con_condition_che_rifiuta():
    """Una Rule con condition che restituisce False non si applica."""
    w = sympy.Wild("w")
    rule = Rule(
        name="rifiuta_sempre",
        description="non si applica mai",
        pattern=w,
        replacement=lambda m: m[w],
        condition=lambda m: False,
    )
    assert apply_rule(rule, sympy.Symbol("x")) is None


def test_rule_con_condition_che_accetta():
    """Una Rule con condition che restituisce True si applica."""
    w = sympy.Wild("w")
    rule = Rule(
        name="accetta_sempre",
        description="si applica sempre",
        pattern=w,
        replacement=lambda m: m[w],
        condition=lambda m: True,
    )
    # Nota: il replacement restituisce l'input, quindi apply_rule
    # restituisce l'input ma make_step lo rifiuterebbe.
    result = apply_rule(rule, sympy.Symbol("x"))
    assert result is not None

def test_rule_senza_modalita_rifiutata():
    with pytest.raises(ValueError, match="pattern-based o function-based"):
        Rule(name="r", description="d")


def test_rule_con_entrambe_le_modalita_rifiutata():
    w = sympy.Wild("w")
    with pytest.raises(ValueError, match="contemporaneamente"):
        Rule(
            name="r",
            description="d",
            pattern=w,
            replacement=lambda m: m[w],
            try_apply=lambda e: None,
        )


def test_rule_from_function_si_applica():
    rule = Rule.from_function(
        name="test_funzione",
        description="restituisce sempre x",
        try_apply=lambda e: sympy.Symbol("x"),
    )
    result = apply_rule(rule, sympy.Symbol("y"))
    assert result == sympy.Symbol("x")


def test_rule_from_function_che_fallisce():
    rule = Rule.from_function(
        name="test_funzione",
        description="fallisce sempre",
        try_apply=lambda e: None,
    )
    assert apply_rule(rule, sympy.Symbol("y")) is None


def test_rule_from_function_che_solleva_eccezione():
    def _boom(e):
        raise RuntimeError("boom")

    rule = Rule.from_function(
        name="test_funzione",
        description="solleva",
        try_apply=_boom,
    )
    # apply_rule cattura l'eccezione e restituisce None.
    assert apply_rule(rule, sympy.Symbol("y")) is None