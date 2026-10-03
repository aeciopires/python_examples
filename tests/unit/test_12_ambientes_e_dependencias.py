"""Testes do módulo 12 - ambientes virtuais e pacotes instalados.

``make test`` roda via ``uv run``, ou seja, DENTRO do ambiente virtual .venv.
"""

from __future__ import annotations

import platform
import sys
from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo

M = "12_ambientes_e_dependencias"


def test_rodando_no_ambiente_virtual() -> None:
    assert carregar_exemplo(M, "ambiente").esta_em_ambiente_virtual() is True


def test_fora_de_um_ambiente_virtual(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", sys.base_prefix)  # simula o Python do sistema
    assert carregar_exemplo(M, "ambiente").esta_em_ambiente_virtual() is False


def test_versao_do_pacote() -> None:
    ambiente = carregar_exemplo(M, "ambiente")
    assert ambiente.versao_do_pacote("pytest") == pytest.__version__
    assert ambiente.versao_do_pacote("pacote-que-nao-existe") is None


def test_ambiente(saida_de: Callable[[str, str], str]) -> None:
    linhas = saida_de(M, "ambiente").splitlines()
    assert linhas[0] == f"Versão do Python: {platform.python_version()}"
    assert linhas[2] == "Em um ambiente virtual? True"
    assert linhas[-1] == "pacote-que-nao-existe: não instalado"
