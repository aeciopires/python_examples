"""Funções de apoio compartilhadas pelos testes.

As pastas dos módulos começam com um número (``01_primeiros_passos``), que
não é um identificador Python válido: ``import modulos.01_primeiros_passos``
é um erro de sintaxe. Por isso ``carregar_exemplo()`` importa cada exemplo
pelo caminho do arquivo, com :mod:`importlib` - veja docs/TESTES.md.

Fonte: https://docs.python.org/pt-br/3/library/importlib.html#importing-a-source-file-directly
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

RAIZ = Path(__file__).resolve().parent.parent
MODULOS = RAIZ / "modulos"


def pasta_exemplos(modulo: str) -> Path:
    """Devolve ``modulos/<modulo>/exemplos``."""
    return MODULOS / modulo / "exemplos"


def todos_os_exemplos() -> list[Path]:
    """Todos os ``modulos/*/exemplos/*.py`` - os mesmos que ``make run-all`` executa."""
    return sorted(MODULOS.glob("*/exemplos/*.py"))


def carregar_exemplo(modulo: str, arquivo: str) -> ModuleType:
    """Importa ``modulos/<modulo>/exemplos/<arquivo>.py`` e devolve o módulo.

    A pasta ``exemplos`` entra temporariamente em ``sys.path`` para que um
    exemplo possa importar outro (módulo 06), como acontece quando você roda
    ``python modulos/06_modulos_e_pacotes/exemplos/usa_meu_modulo.py``.
    """
    pasta = pasta_exemplos(modulo)
    caminho = pasta / f"{arquivo}.py"
    nome = f"exemplo_{modulo}_{arquivo}"
    spec = importlib.util.spec_from_file_location(nome, caminho)
    assert spec is not None and spec.loader is not None, f"não encontrei {caminho}"
    modulo_carregado = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(pasta))
    try:
        spec.loader.exec_module(modulo_carregado)
    finally:
        sys.path.remove(str(pasta))
    return modulo_carregado
