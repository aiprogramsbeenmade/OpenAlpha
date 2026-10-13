"""
Registro centrale delle operazioni matematiche di OpenAlpha.

Ogni operazione si dichiara con il decoratore ``@register``. Il registro
permette di:

- scoprire quali operazioni sono disponibili (``list_operations``),
- recuperarne una per nome (``get_operation``),
- invocarla in modo indiretto, senza che il chiamante (CLI, GUI, API)
  debba conoscere il modulo che la implementa.

Questo è il meccanismo che mantiene il motore indipendente dalle
interfacce: la GUI chiederà al registro l'operazione ``"simplify"``,
non importerà ``operations.algebra.simplify`` direttamente.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from openalpha.core.exceptions import UnsupportedOperationError

# Nomi ammessi: minuscole, cifre, underscore. Deve iniziare con una lettera.
_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True)
class OperationSpec:
    """Descrittore di un'operazione registrata.

    Attributi:
        name: nome univoco dell'operazione (es. ``"simplify"``).
        description: descrizione breve in inglese o italiano, mostrata
            all'utente (CLI, GUI, documentazione).
        function: la funzione Python che implementa l'operazione. Deve
            accettare una stringa di input e restituire un ``Result``.
    """

    name: str
    description: str
    function: Callable[..., object]


# Registro interno. Chiave: nome operazione. Valore: OperationSpec.
_registry: dict[str, OperationSpec] = {}


def register(name: str, description: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Decoratore per registrare un'operazione.

    Uso::

        @register("simplify", "Semplifica un'espressione algebrica")
        def simplify(input_expression: str) -> Result:
            ...

    Solleva:
        ValueError: se il nome è vuoto, non conforme al pattern, o già
            registrato.
    """
    if not name:
        raise ValueError("Il nome dell'operazione non può essere vuoto")
    if not _NAME_PATTERN.match(name):
        raise ValueError(
            f"Nome operazione non valido: {name!r}. "
            "Deve iniziare con una lettera minuscola e contenere solo "
            "lettere minuscole, cifre e underscore."
        )
    if not description:
        raise ValueError(
            f"L'operazione {name!r} richiede una descrizione non vuota"
        )
    if name in _registry:
        raise ValueError(f"Operazione già registrata: {name!r}")

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        _registry[name] = OperationSpec(
            name=name,
            description=description,
            function=func,
        )
        return func

    return decorator


def get_operation(name: str) -> OperationSpec:
    """Restituisce l'``OperationSpec`` associata a ``name``.

    Solleva:
        UnsupportedOperationError: se nessuna operazione è registrata
            con quel nome.
    """
    try:
        return _registry[name]
    except KeyError:
        raise UnsupportedOperationError(
            f"Operazione non supportata: {name!r}. "
            f"Disponibili: {', '.join(list_operations()) or '(nessuna)'}"
        ) from None


def list_operations() -> list[str]:
    """Restituisce i nomi delle operazioni registrate, in ordine alfabetico."""
    return sorted(_registry.keys())


def clear_registry() -> None:
    """Svuota il registro.

    Pensato **solo per i test**: consente di isolare i test che
    registrano operazioni temporanee. Non usare in codice di produzione.
    """
    _registry.clear()