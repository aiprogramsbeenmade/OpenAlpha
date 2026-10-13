"""
Entry point per ``python -m openalpha``.

Delega al modulo ``openalpha.cli.main``. Questo file esiste per
permettere l'esecuzione come modulo (``python -m openalpha ...``)
senza dover installare il package.
"""

from __future__ import annotations

from openalpha.cli.main import main

if __name__ == "__main__":
    raise SystemExit(main())