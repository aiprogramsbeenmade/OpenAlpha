"""
Launcher per OpenAlpha web.

Trova una porta libera, avvia il server Flask, apre il browser.
Non richiede all'utente di sapere cosa sia Flask o come si avvia.

Uso:
    python -m openalpha.web.launcher

Oppure, dal bundle PyInstaller:
    ./OpenAlpha  (Linux)
    OpenAlpha.app (macOS)
    OpenAlpha.exe (Windows)
"""

from __future__ import annotations

import socket
import sys
import threading
import time
import webbrowser


def _trova_porta_libera(start: int = 5000, tentativi: int = 20) -> int:
    """Trova una porta TCP libera a partire da ``start``.

    Prova ``start``, ``start + 1``, ..., ``start + tentativi - 1``.
    Solleva ``RuntimeError`` se nessuna è libera.
    """
    for porta in range(start, start + tentativi):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", porta))
                return porta
            except OSError:
                continue
    raise RuntimeError(
        f"nessuna porta libera tra {start} e {start + tentativi - 1}"
    )


def _apri_browser(url: str) -> None:
    """Apre il browser sull'URL specificato dopo un breve delay."""
    time.sleep(1.0)
    webbrowser.open(url)


def main() -> int:
    """Entry point del launcher. Restituisce l'exit code."""
    from openalpha.web.app import create_app

    try:
        porta = _trova_porta_libera(5001)
    except RuntimeError as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        return 1

    url = f"http://127.0.0.1:{porta}"

    print("=" * 60)
    print("OpenAlpha — Calcolatore matematico locale")
    print("=" * 60)
    print(f"Server avviato su: {url}")
    print("Il browser si aprirà automaticamente.")
    print("Premi Ctrl+C per terminare.")
    print("=" * 60)

    # Apri il browser in un thread separato (daemon, così muore col processo).
    threading.Thread(target=_apri_browser, args=[url], daemon=True).start()

    app = create_app()
    app.run(host="127.0.0.1", port=porta, debug=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())