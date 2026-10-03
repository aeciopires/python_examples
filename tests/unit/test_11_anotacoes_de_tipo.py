"""Testes do módulo 11 - anotações de tipo (e por que elas não são verificadas ao rodar)."""

from __future__ import annotations

from collections.abc import Callable

from tests._helpers import carregar_exemplo

M = "11_anotacoes_de_tipo"


def test_anotacoes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "anotacoes").splitlines() == [
        "42",
        "ana None",
        "15.5 6",
        "7.0",
        "abab",
        "{'numero': <class 'int'>, 'return': <class 'int'>}",
    ]


def test_python_nao_verifica_tipos_ao_executar() -> None:
    dobro = carregar_exemplo(M, "anotacoes").dobro
    assert dobro([1]) == [1, 1]  # anotado como int, mas listas também "multiplicam"
