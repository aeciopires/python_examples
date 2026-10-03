"""Testes do módulo 05 - listas, tuplas, conjuntos, dicionários e compreensões."""

from __future__ import annotations

from collections.abc import Callable

from tests._helpers import carregar_exemplo

M = "05_estruturas_de_dados"


def test_listas(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "listas").splitlines() == [
        "arroz café",
        "['pão', 'arroz', 'feijão', 'café', 'leite']",
        "leite ['pão', 'arroz', 'café']",
        "3 True",
        "[5, 7, 8, 10]",
        "[7, 10, 5, 8]",
        "[10, 8, 7, 5]",
        "[8, 7]",
        "[1, 2, 3, 4]",
        "[1, 2, 3, 4] [1, 2, 3, 4, 5]",
    ]


def test_tuplas(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "tuplas").splitlines() == [
        "3 4",
        "<class 'tuple'> <class 'int'>",
        "03/10/2026",
        "Erro: 'tuple' object does not support item assignment",
    ]


def test_conjuntos(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "conjuntos").splitlines() == [
        "['kiwi', 'maçã', 'uva']",
        "['ana', 'bia', 'caio', 'duda']",
        "['bia']",
        "['ana', 'caio']",
        "True",
    ]


def test_dicionarios(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "dicionarios").splitlines() == [
        "Ana",
        "{'nome': 'Ana', 'idade': 31, 'cidade': 'Recife'}",
        "sem e-mail",
        "nome = Ana",
        "idade = 31",
        "['nome', 'idade'] ['Ana', 31]",
        "{'o': 2, 'rato': 2, 'roeu': 1, 'a': 1, 'roupa': 1}",
    ]


def test_contar_palavras_ignora_maiusculas() -> None:
    contar = carregar_exemplo(M, "dicionarios").contar_palavras
    assert contar("Sol sol SOL lua") == {"sol": 3, "lua": 1}
    assert contar("") == {}


def test_compreensoes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "compreensoes").splitlines() == [
        "[0, 1, 4, 9, 16]",
        "[0, 1, 4, 9, 16]",
        "[2, 4, 6]",
        "{'sol': 3, 'lua': 3, 'estrela': 7}",
        "[3, 7]",
    ]
