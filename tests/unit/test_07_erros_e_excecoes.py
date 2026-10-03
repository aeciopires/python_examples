"""Testes do módulo 07 - exceções."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo

M = "07_erros_e_excecoes"


def test_tratando_excecoes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "tratando_excecoes").splitlines() == [
        "42 None",
        "[finally] dividir(10, 2) terminou",
        "10 / 2 = 5.0",
        "[finally] dividir(1, 0) terminou",
        "não dá para dividir por zero",
        "'5' -> 2.0",
        "'abc' -> ValueError: invalid literal for int() with base 10: 'abc'",
        "None -> TypeError: int() argument must be a string, a bytes-like object or a real "
        "number, not 'NoneType'",
        "'0' -> ZeroDivisionError: division by zero",
    ]


def test_lancando_excecoes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "lancando_excecoes").splitlines() == [
        "70",
        "ValueError: o valor do saque deve ser positivo, recebi -5",
        "SaldoInsuficienteError: saldo 100.00 é menor que o saque 500.00",
    ]


def test_sacar_lanca_a_excecao_certa() -> None:
    exemplo = carregar_exemplo(M, "lancando_excecoes")
    assert exemplo.sacar(100, 100) == 0  # sacar tudo é permitido
    with pytest.raises(exemplo.SaldoInsuficienteError, match="menor que o saque"):
        exemplo.sacar(100, 100.01)
    with pytest.raises(ValueError, match="positivo"):
        exemplo.sacar(100, 0)
