"""
Nodi dell'Abstract Syntax Tree (AST) di OpenAlpha.

L'AST è una rappresentazione strutturata di un'espressione matematica,
prodotta dal parser (T2.2). È indipendente da SymPy: la conversione a
SymPy è compito di T2.3.

Ogni nodo è una dataclass immutabile (``frozen=True``): una volta
costruito, l'albero non cambia. Questo rende più sicuri i passaggi
successivi (conversione, spiegazioni) che non devono modificare
l'input.
"""

from __future__ import annotations

from dataclasses import dataclass


class Node:
    """Base di tutti i nodi dell'AST.

    Non va istanziata direttamente: serve solo come tipo comune per
    l'union dei nodi concreti e per il type checking.
    """

    __slots__ = ()


@dataclass(frozen=True)
class Number(Node):
    """Numero letterale, mantenuto come stringa.

    Non convertiamo a ``int`` o ``float`` per non perdere informazione
    (es. ``1e-3`` è una stringa, non un float approssimato). La
    conversione avverrà in T2.3 al momento di costruire l'oggetto SymPy.

    Attributi:
        value: rappresentazione testuale del numero (es. ``"2"``, ``"3.14"``).
    """

    value: str


@dataclass(frozen=True)
class Symbol(Node):
    """Simbolo: variabile o costante.

    Attributi:
        name: nome del simbolo (es. ``"x"``, ``"pi"``).
    """

    name: str


@dataclass(frozen=True)
class BinaryOp(Node):
    """Operazione binaria.

    Attributi:
        op: operatore (``"+"``, ``"-"``, ``"*"``, ``"/"``, ``"**"``, ``"^"``).
        left: nodo di sinistra.
        right: nodo di destra.
    """

    op: str
    left: Node
    right: Node


@dataclass(frozen=True)
class UnaryOp(Node):
    """Operazione unaria.

    Attributi:
        op: operatore (``"+"``, ``"-"``).
        operand: nodo su cui si applica.
    """

    op: str
    operand: Node


@dataclass(frozen=True)
class FunctionCall(Node):
    """Chiamata di funzione a un argomento.

    Attributi:
        name: nome della funzione (es. ``"sin"``).
        argument: nodo argomento.
    """

    name: str
    argument: Node