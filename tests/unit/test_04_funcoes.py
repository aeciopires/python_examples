"""Testes do módulo 04 - funções."""

from __future__ import annotations

from collections.abc import Callable

from tests._helpers import carregar_exemplo

M = "04_funcoes"


def test_funcoes_basicas(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "funcoes_basicas").splitlines() == [
        "12",
        "Olá, Ana!",
        "Bom dia, Ana!",
        "1 9",
        "Aviso: disco quase cheio",
        "avisar() devolveu: None",
    ]


def test_argumentos(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "argumentos").splitlines() == [
        "Rex é um(a) cachorro de 1 ano(s)",
        "Mimi é um(a) gato de 1 ano(s)",
        "Mimi é um(a) gato de 3 ano(s)",
        "6.0 10.5 0.0",
        "nome: Ana; cidade: Recife",
        "['a', 'b'] ['a', 'b']",
        "['a'] ['b']",
    ]


def test_armadilha_do_valor_padrao_mutavel() -> None:
    argumentos = carregar_exemplo(M, "argumentos")  # módulo novo: lista padrão vazia
    assert argumentos.adicionar_errado("x") == ["x"]
    assert argumentos.adicionar_errado("y") == ["x", "y"]  # a lista "lembrou" do x
    assert argumentos.adicionar_certo("x") == ["x"]
    assert argumentos.adicionar_certo("y") == ["y"]


def test_escopo(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "escopo").splitlines() == ["global", "local", "global", "1 2", "15"]


def test_funcoes_como_valores(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "funcoes_como_valores").splitlines() == [
        "20",
        "25",
        "['Carlos', 'Duda', 'ana', 'bia']",
        "['ana', 'bia', 'Carlos', 'Duda']",
        "['bia', 'ana', 'Duda', 'Carlos']",
        "[2, 4, 6, 8, 10, 12]",
        "[2, 4, 6]",
    ]
