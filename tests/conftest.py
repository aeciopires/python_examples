"""Fixtures compartilhadas por todos os testes (pytest as encontra sozinho).

Fonte: https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo


@pytest.fixture
def saida_de(capsys: pytest.CaptureFixture[str]) -> Callable[[str, str], str]:
    """Executa o main() de um exemplo e devolve tudo o que ele imprimiu.

    Uso: ``saida_de("01_primeiros_passos", "ola_mundo")``.
    """

    def executar(modulo: str, arquivo: str) -> str:
        exemplo = carregar_exemplo(modulo, arquivo)
        capsys.readouterr()  # descarta o que a importação possa ter impresso
        exemplo.main()
        return capsys.readouterr().out

    return executar
