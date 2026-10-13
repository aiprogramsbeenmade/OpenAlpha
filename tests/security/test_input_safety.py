"""
Suite di sicurezza minima per l'input utente.

Verifica che categorie note di input ostili o malformati vengano
sempre rifiutate, e che nessun input causi eccezioni non gestite.

Non è una suite esaustiva: è una rete di sicurezza per le categorie
principali. Ogni categoria è testata con uno o più esempi
rappresentativi.

Regola d'oro: nessun input utente deve mai produrre uno status di
successo (EXACT, APPROXIMATE, PARTIAL) se l'input è ostile.
"""

from __future__ import annotations

import pytest

from openalpha.core.status import ResultStatus
from openalpha.operations.algebra.simplify import simplify


# Stati che indicano un rifiuto: l'input non ha prodotto un risultato
# utilizzabile.
_RIFIUTO = (ResultStatus.ERROR, ResultStatus.UNSUPPORTED)


def _assert_rifiutato(input_expression: str) -> None:
    """Asserisce che l'input venga rifiutato, senza eccezioni.

    Verifica anche che non venga sollevata alcuna eccezione: la
    funzione ``simplify`` deve sempre restituire un ``Result``,
    mai propagare eccezioni.
    """
    result = simplify(input_expression)
    assert result.status in _RIFIUTO, (
        f"input {input_expression!r} non rifiutato: status={result.status}"
    )


# ---------------------------------------------------------------------------
# Categoria 1 — Tentativi di accesso a Python
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("espressione", [
    "__import__('os')",
    "__import__(os)",
    "eval('1+1')",
    "exec('x=1')",
    "open('/etc/passwd')",
    "globals()",
    "locals()",
    "compile('1', '', 'eval')",
])
def test_accesso_a_python_rifiutato(espressione):
    _assert_rifiutato(espressione)


# ---------------------------------------------------------------------------
# Categoria 2 — Accesso ad attributi
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("espressione", [
    "x.__class__",
    "(1).__class__",
    "x.y.z",
    "x.__dict__",
])
def test_accesso_ad_attributi_rifiutato(espressione):
    _assert_rifiutato(espressione)


# ---------------------------------------------------------------------------
# Categoria 3 — Caratteri vietati
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("espressione", [
    "x'y",       # apostrofo
    'x"y',       # virgoletta doppia
    "x; y",      # punto e virgola
    "x & y",     # ampersand
    "x | y",     # pipe
    "x ! y",     # esclamativo
    "x $ y",     # dollaro
    "x @ y",     # chiocciola
    "x \\ y",    # backslash
])
def test_caratteri_vietati_rifiutati(espressione):
    _assert_rifiutato(espressione)


# ---------------------------------------------------------------------------
# Categoria 4 — Input troppo lungo
# ---------------------------------------------------------------------------

def test_input_troppo_lungo_rifiutato():
    # 2000 caratteri, oltre MAX_INPUT_LENGTH = 1000.
    lungo = "x + " * 500 + "x"
    _assert_rifiutato(lungo)


# ---------------------------------------------------------------------------
# Categoria 5 — Espressioni troppo annidate
# ---------------------------------------------------------------------------

def test_espressione_troppo_annidata_rifiutata():
    # 60 unari annidati: 60 UnaryOp, profondità 60 > MAX_DEPTH = 50.
    # Le parentesi non contano: sono token consumati, non nodi AST.
    annidata = "-" * 60 + "x"
    _assert_rifiutato(annidata)


def test_parentesi_ridondanti_non_aumentano_profondita():
    """Le parentesi sono raggruppamenti, non nodi AST.

    Un'espressione con molte parentesi ridondanti deve essere
    accettata (se non supera altri limiti), perché la profondità
    dell'AST è indipendente dal numero di parentesi.
    """
    from openalpha.operations.algebra.simplify import simplify
    risultato = simplify("(" * 30 + "x" + ")" * 30)
    assert risultato.status is ResultStatus.EXACT
    assert risultato.exact == "x"


# ---------------------------------------------------------------------------
# Categoria 6 — Numeri fuori scala
# ---------------------------------------------------------------------------

def test_numero_con_esponente_fuori_scala_rifiutato():
    _assert_rifiutato("1e100000")


def test_numero_con_troppe_cifre_rifiutato():
    _assert_rifiutato("1" * 200)


# ---------------------------------------------------------------------------
# Categoria 7 — Nomi troppo lunghi
# ---------------------------------------------------------------------------

def test_nome_troppo_lungo_rifiutato():
    # 50 caratteri, oltre MAX_NAME_LENGTH = 30.
    nome_lungo = "x" * 50
    _assert_rifiutato(nome_lungo)


# ---------------------------------------------------------------------------
# Categoria 8 — Sintassi incompleta o malformata
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("espressione", [
    "2 +",
    "(x",
    "x)",
    "*",
    "/",
    "()",
    "2 3 )",
])
def test_sintassi_malformata_rifiutata(espressione):
    _assert_rifiutato(espressione)


# ---------------------------------------------------------------------------
# Robustezza: nessun input causa eccezioni non gestite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("espressione", [
    "",
    "   ",
    "\n\t",
    "(((((",
    ")))))",
    "1" * 5000,
    "x" * 5000,
    "!" * 100,
])
def test_nessuna_eccezione_non_gestita(espressione):
    """Verifica che nessun input causi eccezioni fuori controllo.

    ``simplify`` deve sempre restituire un ``Result``, mai propagare
    eccezioni al chiamante. Questo test è la rete di sicurezza
    finale: se fallisce, c'è un percorso di codice che bypassa la
    gestione degli errori.
    """
    result = simplify(espressione)
    assert isinstance(result, type(simplify("x")))  # è un Result
    assert result.status in _RIFIUTO