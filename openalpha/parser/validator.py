"""
Validatore di AST per OpenAlpha.

Dato un AST prodotto dal parser, decide se è accettabile per il
progetto. Il validatore non si occupa di:

- sintassi (già fatta dal parser),
- funzioni ammesse (già fatto dal convertitore ``to_sympy``),
- correttezza matematica (sarà l'operazione a rilevare ``1/0``).

Si occupa di:

- limiti strutturali (lunghezza input, profondità, numero di nodi),
- regole di sicurezza (pattern dei nomi, lunghezza dei nomi, scala dei numeri).

Tutti i limiti sono costanti in cima al modulo: per cambiarli,
basta modificare qui, e i test che li verificano vanno aggiornati
di conseguenza.

Il validatore è separato da parser e convertitore perché è il punto
in cui si applicano **policy** (cosa accettiamo, cosa no). Cambiare
policy non deve toccare né la grammatica né la conversione.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from openalpha.core.exceptions import ValidationError
from openalpha.parser.ast_nodes import (
    BinaryOp,
    FunctionCall,
    Node,
    Number,
    Symbol,
    UnaryOp,
)

# ---------------------------------------------------------------------------
# Limiti di policy (modificabili in un unico punto)
# ---------------------------------------------------------------------------

MAX_INPUT_LENGTH = 1000
"""Lunghezza massima della stringa di input (caratteri).

Un'espressione digitata a mano raramente supera i 200–300 caratteri.
1000 lascia ampio margine e blocca input patologici.
"""

MAX_DEPTH = 50
"""Profondità massima dell'AST.

Copre qualsiasi espressione ragionevole. Oltre, il rischio di stack
overflow nel parser ricorsivo o in SymPy cresce.
"""

MAX_NODES = 500
"""Numero massimo di nodi nell'AST.

Un'espressione di 200 caratteri tipicamente ha 20–30 nodi.
500 dà molto margine e blocca strutture esplosive.
"""

MAX_NAME_LENGTH = 30
"""Lunghezza massima di un nome (variabile o funzione)."""

NAME_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
"""Pattern dei nomi ammessi.

Difesa in profondità: il tokenizer già applica questo pattern, ma
il validatore lo ripete per il caso in cui l'AST arrivi da un'altra
fonte (es. costruzione programmatica in un test futuro).
"""

MAX_DIGITS_IN_NUMBER = 100
"""Numero massimo di cifre in un numero letterale."""

MAX_EXPONENT_ABS = 10000
"""Valore assoluto massimo dell'esponente in notazione scientifica.

``1e9999`` è accettato, ``1e10000`` è rifiutato. Il motivo è evitare
che SymPy tenti di calcolare numeri enormi.
"""


# ---------------------------------------------------------------------------
# Tipi di supporto
# ---------------------------------------------------------------------------

@dataclass
class _Stats:
    """Statistiche raccolte durante la visita dell'AST."""

    max_depth: int = 0
    node_count: int = 0


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------

def validate(node: Node, input_length: int) -> None:
    """Valida un AST secondo le regole di policy di OpenAlpha.

    Args:
        node: radice dell'AST.
        input_length: lunghezza della stringa di input originale.
            Passata separatamente perché l'AST non conserva questa
            informazione.

    Solleva:
        ValidationError: se una qualsiasi regola è violata. Il
            messaggio indica quale regola e, quando utile, il valore
            che l'ha violata.

    Ritorna:
        ``None`` se l'AST è accettabile. Non restituisce l'AST: non
        lo trasforma, si limita a verificarlo.
    """
    if input_length > MAX_INPUT_LENGTH:
        raise ValidationError(
            f"input troppo lungo: {input_length} caratteri "
            f"(massimo {MAX_INPUT_LENGTH})"
        )

    stats = _Stats()
    _check_node(node, depth=0, stats=stats)


# ---------------------------------------------------------------------------
# Visita ricorsiva
# ---------------------------------------------------------------------------

def _check_node(node: Node, depth: int, stats: _Stats) -> None:
    """Visita ricorsivamente l'AST, aggiornando le statistiche e
    sollevando ``ValidationError`` appena una regola è violata.

    L'ordine dei controlli è importante: prima si aggiornano le
    statistiche, poi si verificano i limiti, poi si scende nei figli.
    Così un errore di profondità viene rilevato al nodo giusto.
    """
    stats.node_count += 1
    if depth > stats.max_depth:
        stats.max_depth = depth

    if stats.node_count > MAX_NODES:
        raise ValidationError(
            f"espressione troppo complessa: più di {MAX_NODES} nodi"
        )

    if depth > MAX_DEPTH:
        raise ValidationError(
            f"espressione troppo annidata: profondità {depth} "
            f"(massimo {MAX_DEPTH})"
        )

    if isinstance(node, Number):
        _check_number(node)
        return

    if isinstance(node, Symbol):
        _check_name(node.name)
        return

    if isinstance(node, UnaryOp):
        _check_node(node.operand, depth + 1, stats)
        return

    if isinstance(node, BinaryOp):
        _check_node(node.left, depth + 1, stats)
        _check_node(node.right, depth + 1, stats)
        return

    if isinstance(node, FunctionCall):
        _check_name(node.name)
        _check_node(node.argument, depth + 1, stats)
        return

    # Nodo sconosciuto: non dovrebbe accadere, ma non ci fidiamo.
    raise ValidationError(
        f"tipo di nodo non riconosciuto dal validatore: {type(node).__name__}"
    )


def _check_name(name: str) -> None:
    """Verifica che un nome rispetti le regole di policy."""
    if len(name) > MAX_NAME_LENGTH:
        raise ValidationError(
            f"nome troppo lungo: {len(name)} caratteri "
            f"(massimo {MAX_NAME_LENGTH}): {name!r}"
        )
    if not NAME_PATTERN.match(name):
        raise ValidationError(
            f"nome non conforme al pattern ammesso: {name!r}"
        )


def _check_number(node: Number) -> None:
    """Verifica che un numero letterale rispetti le regole di policy.

    Regole:
    - cifre totali (ignorando punto, segno, esponente) ≤ MAX_DIGITS_IN_NUMBER;
    - se c'è esponente, |esponente| ≤ MAX_EXPONENT_ABS.
    """
    value = node.value

    # Conta le cifre in tutto il numero (incluso esponente).
    digits = sum(1 for ch in value if ch.isdigit())
    if digits > MAX_DIGITS_IN_NUMBER:
        raise ValidationError(
            f"numero con troppe cifre: {digits} "
            f"(massimo {MAX_DIGITS_IN_NUMBER})"
        )

    # Se c'è esponente (e/E), controlla il valore assoluto.
    lowered = value.lower()
    if "e" in lowered:
        _, _, exp_part = lowered.partition("e")
        # exp_part può essere "+5", "-5", "5".
        try:
            exp_value = int(exp_part)
        except ValueError:
            raise ValidationError(
                f"numero con esponente non interpretabile: {value!r}"
            ) from None
        if abs(exp_value) > MAX_EXPONENT_ABS:
            raise ValidationError(
                f"esponente fuori scala: {exp_value} "
                f"(massimo in valore assoluto {MAX_EXPONENT_ABS})"
            )