"""
Gerarchia di eccezioni di OpenAlpha.

Tutte le eccezioni sollevate intenzionalmente dal motore di OpenAlpha
derivano da ``OpenAlphaError``. Questo permette a CLI, GUI e test di
distinguere in modo pulito:

- errori *nostri* (previsti, gestibili),
- errori *di terze parti* (SymPy, NumPy, ...) che non vogliamo far
  trapelare al di fuori del motore.

Regola pratica: nessun modulo di ``operations/`` o ``parser/`` deve
propagare eccezioni di SymPy o di altre librerie esterne oltre il
proprio confine. Vanno tradotte in una delle eccezioni definite qui.
"""

from __future__ import annotations


class OpenAlphaError(Exception):
    """Base di tutte le eccezioni di OpenAlpha.

    Catturare questa eccezione significa catturare *qualsiasi* errore
    intenzionalmente sollevato dal progetto, e nient'altro. Non usare
    ``except Exception`` al posto di questa.
    """


# ---------------------------------------------------------------------------
# Errori di parsing / validazione dell'input
# ---------------------------------------------------------------------------

class ParserError(OpenAlphaError):
    """Errore durante il parsing dell'input matematico.

    Indica che la stringa fornita dall'utente non è stata interpretata
    correttamente: sintassi non riconosciuta, caratteri non ammessi,
    struttura malformata.
    """


class ValidationError(ParserError):
    """Input sintatticamente valido ma rifiutato dalle regole di sicurezza.

    Esempio: espressione troppo lunga, uso di costrutti esplicitamente
    vietati, superamento dei limiti di complessità consentiti.
    Sottoclasse di ``ParserError`` perché il confine è lo stesso:
    l'input non entra nel motore.
    """


# ---------------------------------------------------------------------------
# Errori di esecuzione delle operazioni
# ---------------------------------------------------------------------------

class OperationError(OpenAlphaError):
    """Errore durante l'esecuzione di un'operazione matematica.

    Indica che l'input era valido e l'operazione è stata tentata, ma
    non è giunta a termine: divisione per zero rilevata a runtime,
    timeout, eccezione del motore simbolico tradotta, risultato non
    calcolabile nei limiti imposti.
    """


class UnsupportedOperationError(OperationError):
    """Operazione non supportata da OpenAlpha.

    Non è un errore in senso stretto: è la dichiarazione onesta di un
    limite attuale del motore. Coerente con la regola del progetto:
    se non esiste un procedimento verificato, va dichiarato, non
    inventato.

    Sottoclasse di ``OperationError`` perché il confine è lo stesso:
    l'operazione è stata richiesta legittimamente e non è stata
    completata.
    """