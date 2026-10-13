"""
Test del modello ``Step``.

Verificano: costruzione valida, rifiuto di campi vuoti, rifiuto di
``before == after``, indipendenza dei default, immutabilità,
rappresentazione compatta.
"""

from __future__ import annotations

import pytest

from openalpha.core.step import Step

# ---------------------------------------------------------------------------
# Costruzione valida
# ---------------------------------------------------------------------------

def test_step_minimo():
    s = Step(
        before="(x + 1)**2",
        after="x**2 + 2*x + 1",
        rule_name="square_of_binomial",
        description="Quadrato del binomio",
    )
    assert s.before == "(x + 1)**2"
    assert s.after == "x**2 + 2*x + 1"
    assert s.rule_name == "square_of_binomial"
    assert s.description == "Quadrato del binomio"
    assert s.conditions == []


def test_step_con_condizioni():
    s = Step(
        before="1/x",
        after="x**-1",
        rule_name="negative_exponent",
        description="Esponente negativo",
        conditions=["x != 0"],
    )
    assert s.conditions == ["x != 0"]


# ---------------------------------------------------------------------------
# Rifiuti
# ---------------------------------------------------------------------------

def test_before_vuoto_rifiutato():
    with pytest.raises(ValueError, match="before"):
        Step(
            before="",
            after="x",
            rule_name="rule",
            description="desc",
        )


def test_after_vuoto_rifiutato():
    with pytest.raises(ValueError, match="after"):
        Step(
            before="x",
            after="",
            rule_name="rule",
            description="desc",
        )


def test_rule_name_vuoto_rifiutato():
    with pytest.raises(ValueError, match="rule_name"):
        Step(
            before="a",
            after="b",
            rule_name="",
            description="desc",
        )


def test_description_vuota_rifiutata():
    with pytest.raises(ValueError, match="description"):
        Step(
            before="a",
            after="b",
            rule_name="rule",
            description="",
        )


def test_conditions_none_rifiutato():
    with pytest.raises(ValueError, match="conditions"):
        Step(
            before="a",
            after="b",
            rule_name="rule",
            description="desc",
            conditions=None,  # type: ignore[arg-type]
        )


def test_before_uguale_after_rifiutato():
    with pytest.raises(ValueError, match="identici"):
        Step(
            before="x",
            after="x",
            rule_name="rule",
            description="desc",
        )


# ---------------------------------------------------------------------------
# Indipendenza dei default
# ---------------------------------------------------------------------------

def test_conditions_indipendenti_tra_istanze():
    s1 = Step(before="a", after="b", rule_name="r", description="d")
    s2 = Step(before="c", after="d", rule_name="r", description="d")
    s1.conditions.append("x > 0")
    assert s2.conditions == []


# ---------------------------------------------------------------------------
# Immutabilità
# ---------------------------------------------------------------------------

def test_step_immutabile():
    s = Step(before="a", after="b", rule_name="r", description="d")
    with pytest.raises(Exception):  # FrozenInstanceError è una sottoclasse di AttributeError
        s.before = "nuovo"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------

def test_str_contiene_before_after_rule():
    s = Step(
        before="(x + 1)**2",
        after="x**2 + 2*x + 1",
        rule_name="square_of_binomial",
        description="Quadrato del binomio",
    )
    text = str(s)
    assert "(x + 1)**2" in text
    assert "x**2 + 2*x + 1" in text
    assert "square_of_binomial" in text


def test_str_mostra_condizioni():
    s = Step(
        before="1/x",
        after="x**-1",
        rule_name="negative_exponent",
        description="Esponente negativo",
        conditions=["x != 0"],
    )
    assert "x != 0" in str(s)