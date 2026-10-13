"""
Test del registro delle operazioni.

Verificano: registrazione valida, rifiuto di duplicati e nomi invalidi,
recupero per nome, errore su operazione assente, elenco ordinato,
e isolamento tramite ``clear_registry``.
"""

from __future__ import annotations

import pytest

from openalpha.core.exceptions import UnsupportedOperationError
from openalpha.core.registry import (
    clear_registry,
    get_operation,
    list_operations,
    register,
)
from openalpha.core import registry as _registry_module


@pytest.fixture(autouse=True)
def _isolated_registry():
    """Salva e ripristina il registro attorno a ogni test."""
    saved = dict(_registry_module._registry)
    _registry_module._registry.clear()
    yield
    _registry_module._registry.clear()
    _registry_module._registry.update(saved)


def test_register_valido():
    @register("dummy", "operazione di test")
    def dummy(x: str) -> str:
        return x

    spec = get_operation("dummy")
    assert spec.name == "dummy"
    assert spec.description == "operazione di test"
    assert spec.function is dummy


def test_register_nome_vuoto_rifiutato():
    with pytest.raises(ValueError, match="vuoto"):
        @register("", "descrizione")
        def f(x):  # pragma: no cover
            return x


def test_register_nome_non_conforme_rifiutato():
    with pytest.raises(ValueError, match="non valido"):
        @register("Simplify!", "descrizione")
        def f(x):  # pragma: no cover
            return x


def test_register_descrizione_vuota_rifiutata():
    with pytest.raises(ValueError, match="descrizione"):
        @register("ok_name", "")
        def f(x):  # pragma: no cover
            return x


def test_register_duplicato_rifiutato():
    @register("dup", "prima")
    def f(x):  # pragma: no cover
        return x

    with pytest.raises(ValueError, match="già registrata"):
        @register("dup", "seconda")
        def g(x):  # pragma: no cover
            return x


def test_get_operation_assente_solleva_unsupported():
    with pytest.raises(UnsupportedOperationError, match="non supportata"):
        get_operation("inesistente")


def test_list_operations_ordinata():
    @register("zeta", "z")
    def f(x):  # pragma: no cover
        return x

    @register("alpha", "a")
    def g(x):  # pragma: no cover
        return x

    @register("mu", "m")
    def h(x):  # pragma: no cover
        return x

    assert list_operations() == ["alpha", "mu", "zeta"]


def test_clear_registry_svuota():
    @register("temporanea", "t")
    def f(x):  # pragma: no cover
        return x

    assert "temporanea" in list_operations()
    clear_registry()
    assert list_operations() == []