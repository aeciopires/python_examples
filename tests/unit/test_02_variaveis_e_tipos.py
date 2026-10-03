"""Testes do módulo 02 - as saídas mostradas no README do módulo."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo

M = "02_variaveis_e_tipos"


def test_variaveis(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "variaveis").splitlines() == [
        "Ana 30 1.65 True",
        "Ano que vem: 31",
        "x = 20 e y = 10",
        "<class 'str'> <class 'int'> <class 'float'> <class 'bool'>",
    ]


def test_numeros(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "numeros").splitlines() == [
        "3.5",
        "3",
        "1",
        "-4",
        "1024",
        "1267650600228229401496703205376",
        "0.30000000000000004",
        "0.3",
        "7.5",
    ]


def test_media() -> None:
    numeros = carregar_exemplo(M, "numeros")
    assert numeros.media(7, 8) == 7.5
    # 0.1 + 0.2 não é exatamente 0.3: compare floats com pytest.approx
    assert numeros.media(0.1, 0.2) * 2 == pytest.approx(0.3)


def test_textos(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "textos").splitlines() == [
        "6",
        "P n",
        "Py thon",
        "PYTHON python",
        "True",
        "Python 3.14 é a versão usada nesta trilha.",
        "Pi com 2 casas: 3.14",
        "['banana', 'maçã', 'uva']",
        "banana | maçã | uva",
        "banana,maçã,kiwi",
        "Olá, Ada Lovelace!",
    ]


def test_saudacao_limpa_espacos() -> None:
    assert carregar_exemplo(M, "textos").saudacao("  grace hopper ") == "Olá, Grace Hopper!"


def test_conversoes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "conversoes").splitlines() == [
        "43",
        "7.0",
        "100",
        "3",
        "False False False False",
        "True True True",
        "True",
    ]
