"""
Test della CLI di OpenAlpha.

Verificano: esecuzione base, help, --list, input vuoto, operazione
non supportata, exit code coerenti.

Uso ``capsys`` di pytest per catturare stdout/stderr senza toccare
il terminale reale.
"""

from __future__ import annotations

import pytest

from openalpha.cli.main import main


def test_cli_semplificazione(capsys):
    code = main(["sin(x)**2 + cos(x)**2"])
    out = capsys.readouterr().out
    assert code == 0
    assert "input:" in out
    assert "sin(x)**2 + cos(x)**2" in out
    assert "status:      exact" in out
    assert "exact:       1" in out


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "openalpha" in out
    assert "--operation" in out


def test_cli_list(capsys):
    code = main(["--list"])
    out = capsys.readouterr().out
    assert code == 0
    assert "simplify" in out
    assert "Operazioni disponibili" in out


def test_cli_input_vuoto(capsys):
    code = main([""])
    captured = capsys.readouterr()
    assert code == 1
    assert "error:" in captured.out


def test_cli_operazione_non_supportata(capsys):
    code = main(["--operation", "inesistente", "x"])
    captured = capsys.readouterr()
    assert code == 2
    assert "non supportata" in captured.err


def test_cli_manca_espressione(capsys):
    code = main([])
    captured = capsys.readouterr()
    assert code == 2
    assert "manca l'espressione" in captured.err

def test_cli_limit_con_var_e_point(capsys):
    code = main(["--operation", "limit", "--var", "x", "--point", "0", "sin(x)/x"])
    out = capsys.readouterr().out
    assert code == 0
    assert "exact:       1" in out


def test_cli_limit_default(capsys):
    code = main(["--operation", "limit", "sin(x)/x"])
    out = capsys.readouterr().out
    assert code == 0
    assert "exact:       1" in out

def test_cli_diff_semplice(capsys):
    code = main(["--operation", "diff", "sin(x)"])
    out = capsys.readouterr().out
    assert code == 0
    assert "exact:       cos(x)" in out


def test_cli_diff_con_order(capsys):
    code = main(["--operation", "diff", "--order", "2", "x**3"])
    out = capsys.readouterr().out
    assert code == 0
    assert "exact:       6*x" in out


def test_cli_diff_order_invalido(capsys):
    code = main(["--operation", "diff", "--order", "abc", "x"])
    captured = capsys.readouterr()
    assert code == 2
    assert "intero" in captured.err

def test_cli_integrate_indefinito(capsys):
    code = main(["--operation", "integrate", "x"])
    out = capsys.readouterr().out
    assert code == 0
    assert "x**2/2 + C" in out


def test_cli_integrate_definito(capsys):
    code = main([
        "--operation", "integrate",
        "--from", "0", "--to", "1",
        "x",
    ])
    out = capsys.readouterr().out
    assert code == 0
    assert "1/2" in out


def test_cli_integrate_solo_from(capsys):
    code = main(["--operation", "integrate", "--from", "0", "x"])
    captured = capsys.readouterr()
    # L'errore d'uso è catturato da integrate e restituito come
    # Result(status=ERROR), quindi exit code 1.
    assert code == 1
    assert "entrambi" in captured.out

def test_cli_nsolve(capsys):
    code = main(["--operation", "nsolve", "x**2 - 2"])
    out = capsys.readouterr().out
    assert code == 0
    assert "approximate:" in out
    assert "1.41421" in out


def test_cli_nsolve_con_initial(capsys):
    code = main(["--operation", "nsolve", "--initial", "-1", "x**2 - 2"])
    out = capsys.readouterr().out
    assert code == 0
    assert "-1.41421" in out


def test_cli_nintegrate(capsys):
    code = main([
        "--operation", "nintegrate",
        "--from", "0", "--to", "1",
        "exp(-x**2)",
    ])
    out = capsys.readouterr().out
    assert code == 0
    assert "0.7468" in out

def test_cli_plot(capsys, tmp_path):
    output = str(tmp_path / "test_plot.png")
    # Non possiamo passare --output dalla CLI (non è ancora implementato),
    # quindi testiamo solo che il comando non crasha.
    # Il file sarà generato nella directory corrente.
    code = main(["--operation", "plot", "sin(x)"])
    out = capsys.readouterr().out
    assert code == 0
    assert "exact:" in out
    # Pulisci il file generato.
    import os
    for line in out.splitlines():
        if line.startswith("exact:"):
            path = line.replace("exact:", "").strip()
            if os.path.exists(path):
                os.remove(path)