"""
Stati possibili di un risultato di calcolo in OpenAlpha.

Questo modulo definisce l'unico insieme di stati ammessi per un
``Result``. Ogni operazione matematica deve dichiarare in modo
esplicito lo stato del proprio output: non è consentito omettere
questa informazione né inventare stati ad hoc altrove nel codice.

La distinzione fondamentale è tra risultato **esatto** e risultato
**approssimato**. Un'approssimazione numerica non deve mai essere
presentata come risultato esatto.
"""

from __future__ import annotations

from enum import Enum


class ResultStatus(str, Enum):
    """Stato di un risultato di calcolo.

    Eredita da ``str`` per rendere banale la serializzazione (JSON,
    logging, confronti con stringhe) senza perdere la type-safety
    dell'enum.
    """

    EXACT = "exact"
    """Risultato esatto e completo.

    Esempio: ``simplify(sin(x)**2 + cos(x)**2)`` → ``1``.
    Il risultato è matematicamente equivalente all'input, senza
    perdita di informazione.
    """

    APPROXIMATE = "approximate"
    """Risultato approssimato numericamente.

    Esempio: ``pi`` valutato come ``3.14159265...``.
    Il risultato è utile ma non è la verità matematica completa:
    rappresenta un valore numerico con precisione finita.
    """

    PARTIAL = "partial"
    """Risultato parziale o condizionato.

    Esempio: soluzione di un'equazione con condizioni sul dominio,
    oppure risultato valido solo sotto ipotesi esplicite.
    Le condizioni vanno sempre riportate insieme al risultato.
    """

    ERROR = "error"
    """Il calcolo è fallito.

    L'input era formalmente valido ma l'operazione non è stata
    completata (es. divisione per zero rilevata a runtime,
    timeout, eccezione del motore simbolico).
    I dettagli vanno nel campo ``error`` del ``Result``.
    """

    UNSUPPORTED = "unsupported"
    """Operazione non supportata da OpenAlpha.

    Esempio: l'utente chiede un tipo di calcolo che il motore non
    implementa ancora. Non è un errore: è una dichiarazione onesta
    di limite. Coerente con la regola "non inventare procedimenti".
    """

    def __str__(self) -> str:
        return self.value