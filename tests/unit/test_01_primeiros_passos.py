"""Testes do módulo 01 - as saídas mostradas no README do módulo."""

from __future__ import annotations

from collections.abc import Callable

M = "01_primeiros_passos"


def test_ola_mundo(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "ola_mundo") == "Olá, mundo!\n"


def test_print_e_comentarios(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "print_e_comentarios").splitlines() == [
        "Python é divertido",
        "2026-10-03",
        "Sem pular linha... continuou na mesma linha.",
        "14",
        "20",
    ]


def test_indentacao(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "indentacao").splitlines() == [
        "Esta linha está DENTRO do if (recuada 4 espaços).",
        "Esta também: só rodam se a condição for verdadeira.",
        "Esta linha está FORA do if: roda sempre.",
    ]
