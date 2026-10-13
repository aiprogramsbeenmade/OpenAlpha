"""
Test del launcher (senza avviare effettivamente il server).
"""

from __future__ import annotations

import socket

import pytest

from openalpha.web.launcher import _trova_porta_libera


def test_trova_porta_libera_default():
    """Trova una porta libera a partire da 5000."""
    porta = _trova_porta_libera(5000)
    assert 5000 <= porta < 5020


def test_trova_porta_libera_salta_occupata():
    """Se la porta di partenza è occupata, ne trova un'altra."""
    # Trova una porta libera dinamicamente.
    base = 56000
    for candidato in range(base, base + 100):
        if _tre_porte_libere(candidato):
            base = candidato
            break
    else:
        pytest.skip("nessun range di 3 porte libere consecutive trovato")

    # Occupa la prima porta del range.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", base))
        s.listen(1)
        porta = _trova_porta_libera(base)
        assert porta != base
        assert base < porta < base + 20


def _tre_porte_libere(base: int) -> bool:
    """Verifica che le porte base, base+1, base+2 siano tutte libere."""
    sockets = []
    try:
        for p in range(base, base + 3):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", p))
            sockets.append(s)
        return True
    except OSError:
        return False
    finally:
        for s in sockets:
            s.close()


def test_trova_porta_libera_nessuna_disponibile():
    """Se tutte le porte sono occupate, solleva RuntimeError.

    Trova dinamicamente 3 porte libere consecutive, le occupa, e
    verifica che `_trova_porta_libera` fallisca su quel range.

    Questo evita di hardcodare porte che potrebbero essere riservate
    dal sistema (es. macOS usa 5000 e 7000 per AirPlay).
    """
    base = 55000
    for candidato in range(base, base + 100):
        if _tre_porte_libere(candidato):
            base = candidato
            break
    else:
        pytest.skip("nessun range di 3 porte libere consecutive trovato")

    sockets = []
    try:
        for p in range(base, base + 3):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", p))
            s.listen(1)
            sockets.append(s)
        with pytest.raises(RuntimeError, match="nessuna porta libera"):
            _trova_porta_libera(base, tentativi=3)
    finally:
        for s in sockets:
            s.close()