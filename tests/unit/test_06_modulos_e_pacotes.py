"""Testes do módulo 06 - módulos, pacotes e a biblioteca padrão."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

from tests._helpers import carregar_exemplo

M = "06_modulos_e_pacotes"


def test_meu_modulo_importado_nao_executa_main(saida_de: Callable[[str, str], str]) -> None:
    # Ao ser carregado pelos testes, __name__ NÃO é "__main__".
    saida = saida_de(M, "meu_modulo")
    assert saida.splitlines()[1] == "42"
    assert "__main__" not in saida


def test_usa_meu_modulo(saida_de: Callable[[str, str], str]) -> None:
    linhas = saida_de(M, "usa_meu_modulo").splitlines()
    assert linhas[:3] == [
        "Olá do meu_modulo!",
        "10 14",
        "__name__ do módulo importado: 'meu_modulo'",
    ]


def test_usa_pacote(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "usa_pacote").splitlines() == [
        "Área do círculo de raio 2: 12.57",
        "Área do quadrado de lado 3: 9",
    ]


def test_biblioteca_padrao(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "biblioteca_padrao").splitlines() == [
        "4.0 2 3",
        "3.14159",
        "7.75 7.75",
        "[('a', 5), ('b', 2)]",
        "358",
        "2026-10-03",
    ]


def test_dias_entre() -> None:
    dias_entre = carregar_exemplo(M, "biblioteca_padrao").dias_entre
    assert dias_entre(date(2026, 2, 28), date(2026, 3, 1)) == 1
    assert dias_entre(date(2028, 2, 28), date(2028, 3, 1)) == 2  # 2028 é bissexto
