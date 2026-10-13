"""
Modello di un singolo passo di un procedimento matematico.

Uno ``Step`` rappresenta una transizione da un'espressione a un'altra,
con una regola applicata e una descrizione leggibile. Una sequenza di
``Step`` forma una spiegazione.

Il modello è volutamente **indipendente da SymPy**: ``before`` e ``after``
sono stringhe. La verifica matematica del passo avviene nel codice che
genera lo ``Step`` (``explanations/rules.py``), non nel modello stesso.

Uno ``Step`` è immutabile (``frozen=True``): una volta costruito e
verificato, non cambia.

**Nota architetturale**: questo modulo vive in ``core/`` e non in
``explanations/`` perché ``Step`` è un dato del motore, non una
spiegazione "ricca". Spostarlo qui mantiene ``core/`` indipendente
da SymPy: ``explanations/rules.py`` (che usa SymPy) importa ``Step``
da qui, non viceversa.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Step:
    """Un singolo passo di un procedimento matematico.

    Attributi:
        before: espressione prima del passo.
        after: espressione dopo il passo.
        rule_name: identificatore univoco della regola applicata
            (es. ``"square_of_binomial"``). Non è il testo mostrato
            all'utente: per quello c'è ``description``.
        description: testo leggibile che spiega cosa è stato fatto.
        conditions: condizioni di validità del passo (es. ``"x != 0"``).
            Lista vuota se non ve ne sono.
    """

    before: str
    after: str
    rule_name: str
    description: str
    conditions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.before:
            raise ValueError("'before' non può essere vuoto")
        if not self.after:
            raise ValueError("'after' non può essere vuoto")
        if not self.rule_name:
            raise ValueError("'rule_name' non può essere vuoto")
        if not self.description:
            raise ValueError("'description' non può essere vuota")
        if self.conditions is None:
            raise ValueError("'conditions' non può essere None, usare lista vuota")
        if self.before == self.after:
            raise ValueError(
                "'before' e 'after' non possono essere identici: "
                "uno Step che non cambia nulla è sospetto"
            )

    def __str__(self) -> str:
        parts = [f"{self.before} → {self.after}", f"({self.rule_name})"]
        if self.conditions:
            parts.append(f"[{', '.join(self.conditions)}]")
        return " ".join(parts)