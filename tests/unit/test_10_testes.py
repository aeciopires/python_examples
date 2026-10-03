"""Módulo 10 - testes com pytest, comentados linha a linha.

Este arquivo É o conteúdo do módulo 10: leia junto com
modulos/10_testes/README.md.

Fontes:
- https://docs.pytest.org/en/stable/getting-started.html
- https://docs.pytest.org/en/stable/how-to/assert.html
- https://docs.pytest.org/en/stable/how-to/parametrize.html
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx
- https://docs.python.org/pt-br/3/library/doctest.html
"""

from __future__ import annotations

import doctest
from collections.abc import Callable
from types import ModuleType

import pytest

from tests._helpers import carregar_exemplo

M = "10_testes"


# 1. Uma FIXTURE prepara algo que vários testes usam. O pytest a injeta em
#    todo teste que tiver um parâmetro com o mesmo nome ("calc").
@pytest.fixture
def calc() -> ModuleType:
    return carregar_exemplo(M, "calculadora")


# 2. O teste mais simples: uma função que começa com "test_" e usa assert.
def test_somar(calc: ModuleType) -> None:
    assert calc.somar(2, 3) == 5


# 3. PARAMETRIZE: o mesmo teste com várias entradas - cada linha vira um teste.
@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (1_000_000, 1, 1_000_001),
    ],
)
def test_somar_varios_casos(calc: ModuleType, a: int, b: int, esperado: int) -> None:
    assert calc.somar(a, b) == esperado


# 4. FLOATS: 0.1 + 0.2 != 0.3 (módulo 02). Use pytest.approx.
def test_somar_floats(calc: ModuleType) -> None:
    assert calc.somar(0.1, 0.2) == pytest.approx(0.3)


# 5. EXCEÇÕES: pytest.raises verifica que o erro certo acontece.
def test_dividir_por_zero(calc: ModuleType) -> None:
    with pytest.raises(ZeroDivisionError, match="dividir 1 por zero"):
        calc.dividir(1, 0)


def test_media_de_lista_vazia(calc: ModuleType) -> None:
    with pytest.raises(ValueError):
        calc.media([])


# 6. LIMITES: teste exatamente nas fronteiras da regra (4.99, 5, 6.99, 7).
@pytest.mark.parametrize(
    ("nota", "esperado"),
    [
        (0, "reprovado"),
        (4.99, "reprovado"),
        (5, "recuperação"),
        (6.99, "recuperação"),
        (7, "aprovado"),
        (10, "aprovado"),
    ],
)
def test_situacao_nos_limites(calc: ModuleType, nota: float, esperado: str) -> None:
    assert calc.situacao(nota) == esperado


@pytest.mark.parametrize("nota", [-0.1, 10.1])
def test_situacao_rejeita_nota_invalida(calc: ModuleType, nota: float) -> None:
    with pytest.raises(ValueError, match="fora do intervalo"):
        calc.situacao(nota)


# 7. CAPSYS: captura o que foi impresso com print().
def test_main_imprime(capsys: pytest.CaptureFixture[str], calc: ModuleType) -> None:
    calc.main()
    assert capsys.readouterr().out == "5 2.5 8.0\nreprovado recuperação aprovado\n"


# 8. DOCTEST: roda os exemplos ">>>" das docstrings como testes.
def test_doctests_da_calculadora(calc: ModuleType) -> None:
    resultado = doctest.testmod(calc)
    assert resultado.attempted == 5
    assert resultado.failed == 0


# A fixture "saida_de" vem de tests/conftest.py (compartilhada por todos os testes).
def test_saida_com_fixture_compartilhada(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "calculadora").startswith("5 ")
