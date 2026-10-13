"""
Test del validatore di AST.

Verificano: accettazione di input normali, rifiuto per input troppo
lungo, profondità eccessiva, numero eccessivo di nodi, nomi non
conformi, numeri fuori scala.
"""

from __future__ import annotations

import pytest

from openalpha.core.exceptions import ValidationError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Number,
    Symbol,
    UnaryOp,
)
from openalpha.parser.parser import parse_tokens
from openalpha.parser.tokenizer import tokenize
from openalpha.parser.validator import (
    MAX_DEPTH,
    MAX_EXPONENT_ABS,
    MAX_INPUT_LENGTH,
    MAX_NAME_LENGTH,
    MAX_NODES,
    validate,
)


def _parse(s: str):
    return parse_tokens(tokenize(s))


def _validate_str(s: str) -> None:
    """Utility: parsa e valida una stringa."""
    validate(_parse(s), input_length=len(s))


# ---------------------------------------------------------------------------
# Casi accettati
# ---------------------------------------------------------------------------

def test_input_semplice_accettato():
    _validate_str("x + 1")


def test_input_composto_accettato():
    _validate_str("sin(x)**2 + cos(x)**2")


def test_funzione_annidata_accettata():
    _validate_str("sin(cos(tan(x)))")


def test_unario_accettato():
    _validate_str("-x + +y")


# ---------------------------------------------------------------------------
# Lunghezza input
# ---------------------------------------------------------------------------

def test_input_troppo_lungo_rifiutato():
    with pytest.raises(ValidationError, match="troppo lungo"):
        validate(Symbol("x"), input_length=MAX_INPUT_LENGTH + 1)


def test_input_al_limite_accettato():
    validate(Symbol("x"), input_length=MAX_INPUT_LENGTH)


# ---------------------------------------------------------------------------
# Profondità
# ---------------------------------------------------------------------------

def test_profondita_al_limite_accettata():
    # Costruiamo manualmente un AST a profondità esattamente MAX_DEPTH
    # con un unario annidato, che è il caso più economico.
    node = Symbol("x")
    for _ in range(MAX_DEPTH):
        node = UnaryOp("-", node)
    validate(node, input_length=1)


def test_profondita_eccessiva_rifiutata():
    node = Symbol("x")
    for _ in range(MAX_DEPTH + 1):
        node = UnaryOp("-", node)
    with pytest.raises(ValidationError, match="annidata"):
        validate(node, input_length=1)


# ---------------------------------------------------------------------------
# Numero di nodi
# ---------------------------------------------------------------------------

def _build_balanced_tree(depth: int) -> Node:
    """Costruisce un albero binario completo di profondità ``depth``.

    Un albero binario completo di profondità d ha 2^(d+1) - 1 nodi.
    Le foglie sono ``Symbol("x")``, i nodi interni sono ``BinaryOp("+")``.
    """
    if depth == 0:
        return Symbol("x")
    return BinaryOp("+", _build_balanced_tree(depth - 1), _build_balanced_tree(depth - 1))


def test_albero_bilanciato_sotto_il_limite_accettato():
    # Profondità 7: 2^8 - 1 = 255 nodi. Sotto MAX_NODES = 500.
    node = _build_balanced_tree(7)
    validate(node, input_length=1)


def test_albero_bilanciato_sopra_il_limite_rifiutato():
    # Profondità 9: 2^10 - 1 = 1023 nodi. Sopra MAX_NODES = 500.
    # Profondità 9 < MAX_DEPTH = 50, quindi il rifiuto arriva per nodi.
    node = _build_balanced_tree(9)
    with pytest.raises(ValidationError, match="troppo complessa"):
        validate(node, input_length=1)


def test_catena_lunga_rifiutata_per_profondita():
    # Catena lineare: 60 BinaryOp annidati. Profondità 60 > MAX_DEPTH = 50.
    # Il rifiuto arriva per profondità, anche se i nodi totali sono pochi.
    node = Symbol("x")
    for _ in range(60):
        node = BinaryOp("+", node, Number("1"))
    with pytest.raises(ValidationError, match="annidata"):
        validate(node, input_length=1)


# ---------------------------------------------------------------------------
# Nomi
# ---------------------------------------------------------------------------

def test_nome_al_limite_accettato():
    name = "x" * MAX_NAME_LENGTH
    validate(Symbol(name), input_length=1)


def test_nome_troppo_lungo_rifiutato():
    name = "x" * (MAX_NAME_LENGTH + 1)
    with pytest.raises(ValidationError, match="troppo lungo"):
        validate(Symbol(name), input_length=1)


def test_nome_con_carattere_non_ammesso_rifiutato():
    # Costruito a mano: il parser non lo produrrebbe mai.
    with pytest.raises(ValidationError, match="pattern"):
        validate(Symbol("x-y"), input_length=1)


def test_nome_funzione_troppo_lungo_rifiutato():
    name = "f" * (MAX_NAME_LENGTH + 1)
    node = FunctionCall(name, Symbol("x"))
    with pytest.raises(ValidationError, match="troppo lungo"):
        validate(node, input_length=1)


# ---------------------------------------------------------------------------
# Numeri
# ---------------------------------------------------------------------------

def test_numero_normale_accettato():
    validate(Number("3.14"), input_length=4)


def test_numero_troppe_cifre_rifiutato():
    with pytest.raises(ValidationError, match="troppe cifre"):
        validate(Number("1" * 200), input_length=200)


def test_esponente_fuori_scala_rifiutato():
    with pytest.raises(ValidationError, match="fuori scala"):
        validate(Number(f"1e{MAX_EXPONENT_ABS + 1}"), input_length=20)


def test_esponente_al_limite_accettato():
    validate(Number(f"1e{MAX_EXPONENT_ABS}"), input_length=20)


def test_esponente_negativo_fuori_scala_rifiutato():
    with pytest.raises(ValidationError, match="fuori scala"):
        validate(Number(f"1e-{MAX_EXPONENT_ABS + 1}"), input_length=20)


# ---------------------------------------------------------------------------
# Integrazione con parser
# ---------------------------------------------------------------------------

def test_espressione_reale_accettata():
    _validate_str("(x + 1) * (x - 1) / 2")


def test_espressione_insolita_ma_valida_accettata():
    # Sintatticamente valida, nessuna funzione speciale.
    _validate_str("x x x x")