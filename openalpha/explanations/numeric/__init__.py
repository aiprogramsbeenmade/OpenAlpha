"""
Spiegazioni numeriche: passi di calcolo per operazioni su interi.

Ogni modulo in questo pacchetto esporta una funzione
``explain_<operazione>(...) -> list[Step]`` che descrive l'algoritmo
passo-passo. Le operazioni chiamano queste funzioni e passano la lista
al campo ``steps`` del ``Result``.
"""

from __future__ import annotations