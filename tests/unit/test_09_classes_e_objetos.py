"""Testes do módulo 09 - classes, herança e dataclasses."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo

M = "09_classes_e_objetos"


def test_classes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "classes").splitlines() == [
        "False True",
        "Conta de Ana: R$ 130.00",
        "Conta de Bia: R$ 0.00",
        "[ContaBancaria('Ana', 130), ContaBancaria('Bia', 0.0)]",
        "Banco Exemplo Banco Exemplo",
        "True",
    ]


def test_cada_conta_tem_seu_saldo() -> None:
    conta = carregar_exemplo(M, "classes").ContaBancaria
    a, b = conta("A", 10), conta("B", 10)
    a.depositar(5)
    assert (a.saldo, b.saldo) == (15, 10)
    with pytest.raises(ValueError):
        a.depositar(-1)


def test_heranca(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "heranca").splitlines() == [
        "Nemo vive entre as anêmonas.",
        "ósseo | cartilaginoso",
        "Nemo está nadando. Nemo consegue nadar de ré.",
        "Bruce está nadando. Bruce não nada de ré, mas consegue afundar de ré.",
        "True True",
    ]


def test_dataclasses(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "dataclasses_exemplo").splitlines() == [
        "Produto(nome='Café', preco=18.5, quantidade=2)",
        "True",
        "Total: R$ 44.50",
        "FrozenInstanceError - cannot assign to field 'x'",
    ]


def test_carrinhos_nao_compartilham_itens() -> None:
    exemplo = carregar_exemplo(M, "dataclasses_exemplo")
    um, outro = exemplo.Carrinho(), exemplo.Carrinho()
    um.itens.append(exemplo.Produto("x", 1.0, 1))
    assert outro.itens == []  # default_factory cria uma lista nova para cada carrinho
