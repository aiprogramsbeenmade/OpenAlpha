"""
Modello standardizzato del risultato di un calcolo in OpenAlpha.

Ogni operazione matematica restituisce un ``Result``. La struttura è
volutamente piatta e serializzabile: nessun oggetto SymPy, nessuna
struttura ricorsiva, nessuna dipendenza esterna.

La coerenza tra ``status`` e gli altri campi è garantita da
``__post_init__``.

I passi del procedimento sono ``Step`` (definiti in ``core/step.py``).
I risultati di equazioni sono in ``solutions`` (lista di stringhe).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from openalpha.core.status import ResultStatus
from openalpha.core.step import Step


@dataclass
class Result:
    """Risultato standardizzato di un'operazione matematica.

    Attributi:
        input_expression: stringa originale fornita dall'utente.
        operation: nome dell'operazione eseguita.
        status: stato del calcolo.
        exact: risultato esatto, se disponibile.
        approximate: risultato approssimato, se disponibile.
        solutions: soluzioni di un'equazione, se l'operazione è
            di tipo "solve". Lista vuota altrimenti. Ogni elemento
            è una stringa (es. ``"x = -1"`` o ``"-1"``).
        steps: passi del procedimento, come oggetti ``Step``.
        conditions: condizioni di validità del risultato.
        error: messaggio d'errore, se ``status`` è ``ERROR``.
        metadata: informazioni aggiuntive libere.
    """

    input_expression: str
    operation: str
    status: ResultStatus
    exact: str | None = None
    approximate: str | float | None = None
    solutions: list[str] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Campi obbligatori non vuoti.
        if not self.input_expression and self.status != ResultStatus.ERROR:
            raise ValueError(
                "input_expression non può essere vuoto se status != ERROR"
            )
        if not self.operation:
            raise ValueError("operation non può essere vuota")

        # Coerenza per ERROR
        if self.status == ResultStatus.ERROR:
            if not self.error:
                raise ValueError(
                    "status=ERROR richiede un messaggio in 'error'"
                )
            if self.exact is not None or self.approximate is not None:
                raise ValueError(
                    "status=ERROR non ammette 'exact' né 'approximate'"
                )

        # Coerenza per EXACT
        if self.status == ResultStatus.EXACT:
            if not self.exact and not self.solutions:
                raise ValueError(
                    "status=EXACT richiede un valore in 'exact' o in 'solutions'"
                )
            if self.error is not None:
                raise ValueError(
                    "status=EXACT non ammette un messaggio in 'error'"
                )

        # Coerenza per APPROXIMATE
        if self.status == ResultStatus.APPROXIMATE:
            if self.approximate is None:
                raise ValueError(
                    "status=APPROXIMATE richiede un valore in 'approximate'"
                )
            if self.error is not None:
                raise ValueError(
                    "status=APPROXIMATE non ammette un messaggio in 'error'"
                )

        # Coerenza per UNSUPPORTED
        if self.status == ResultStatus.UNSUPPORTED:
            if self.exact is not None or self.approximate is not None:
                raise ValueError(
                    "status=UNSUPPORTED non ammette 'exact' né 'approximate'"
                )
            if self.solutions:
                raise ValueError(
                    "status=UNSUPPORTED non ammette 'solutions'"
                )

        # Coerenza per PARTIAL
        if self.status == ResultStatus.PARTIAL:
            if self.exact is None and self.approximate is None and not self.solutions:
                raise ValueError(
                    "status=PARTIAL richiede almeno 'exact', 'approximate' "
                    "o 'solutions'"
                )

        # Campi mai None
        if self.solutions is None:
            raise ValueError("'solutions' non può essere None, usare lista vuota")
        if self.steps is None:
            raise ValueError("'steps' non può essere None, usare lista vuota")
        if self.conditions is None:
            raise ValueError("'conditions' non può essere None, usare lista vuota")
        if self.metadata is None:
            raise ValueError("'metadata' non può essere None, usare dict vuoto")

        # Ogni elemento di solutions deve essere stringa non vuota
        for i, sol in enumerate(self.solutions):
            if not isinstance(sol, str):
                raise ValueError(
                    f"'solutions[{i}]' deve essere stringa, "
                    f"trovato {type(sol).__name__}"
                )
            if not sol:
                raise ValueError(f"'solutions[{i}]' non può essere vuota")

        # Ogni elemento di steps deve essere uno Step
        for i, step in enumerate(self.steps):
            if not isinstance(step, Step):
                raise ValueError(
                    f"'steps[{i}]' deve essere uno Step, "
                    f"trovato {type(step).__name__}"
                )

    def is_success(self) -> bool:
        """True se il calcolo ha prodotto un risultato utilizzabile."""
        return self.status not in (
            ResultStatus.ERROR,
            ResultStatus.UNSUPPORTED,
        )

    def __str__(self) -> str:
        """Rappresentazione compatta per log e debug."""
        parts = [f"[{self.status.value}]", self.operation]
        if self.exact is not None:
            parts.append(f"exact={self.exact!r}")
        if self.approximate is not None:
            parts.append(f"approx={self.approximate!r}")
        if self.solutions:
            parts.append(f"solutions={len(self.solutions)}")
        if self.steps:
            parts.append(f"steps={len(self.steps)}")
        if self.error is not None:
            parts.append(f"error={self.error!r}")
        return " ".join(parts)