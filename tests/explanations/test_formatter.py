"""
Test del formatter dei passi.
"""

from __future__ import annotations

from openalpha.core.step import Step
from openalpha.explanations.formatter import format_step, format_steps


def _step_esempio() -> Step:
    return Step(
        before="(x + 1)**2",
        after="x**2 + 2*x + 1",
        rule_name="square_of_binomial",
        description="Applico il quadrato del binomio",
    )


def _step_con_condizioni() -> Step:
    return Step(
        before="1/x",
        after="x**-1",
        rule_name="negative_exponent",
        description="Riscrivo con esponente negativo",
        conditions=["x != 0"],
    )


# ---------------------------------------------------------------------------
# format_step
# ---------------------------------------------------------------------------

def test_format_step_senza_numero():
    text = format_step(_step_esempio())
    assert "Applico il quadrato del binomio" in text
    assert "(x + 1)**2" in text
    assert "x**2 + 2*x + 1" in text
    assert "Passo" not in text


def test_format_step_con_numero():
    text = format_step(_step_esempio(), number=3)
    assert text.startswith("Passo 3:")


def test_format_step_con_condizioni():
    text = format_step(_step_con_condizioni())
    assert "x != 0" in text
    assert "condizioni:" in text


def test_format_step_senza_condizioni_non_mostra_riga():
    text = format_step(_step_esempio())
    assert "condizioni" not in text


# ---------------------------------------------------------------------------
# format_steps
# ---------------------------------------------------------------------------

def test_format_steps_lista_vuota():
    assert format_steps([]) == ""


def test_format_steps_un_passo():
    text = format_steps([_step_esempio()])
    assert "Passo 1:" in text
    assert "Passo 2:" not in text


def test_format_steps_due_passi():
    text = format_steps([_step_esempio(), _step_con_condizioni()])
    assert "Passo 1:" in text
    assert "Passo 2:" in text


def test_format_steps_senza_numerazione():
    text = format_steps([_step_esempio(), _step_con_condizioni()], numbered=False)
    assert "Passo" not in text
    assert "Applico il quadrato del binomio" in text
    assert "Riscrivo con esponente negativo" in text


def test_format_steps_separa_con_riga_vuota():
    text = format_steps([_step_esempio(), _step_con_condizioni()])
    assert "\n\n" in text