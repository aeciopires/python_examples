"""Todo exemplo roda do começo ao fim, como em ``make run-all``, sem erros.

Cada arquivo é executado em um processo separado, do mesmo jeito que você
o executaria no terminal. A entrada padrão é vazia (sem teclado).

Fonte: https://docs.python.org/pt-br/3/library/subprocess.html#subprocess.run
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests._helpers import RAIZ, todos_os_exemplos


def test_existem_exemplos() -> None:
    assert len(todos_os_exemplos()) >= 30


@pytest.mark.parametrize(
    "exemplo", todos_os_exemplos(), ids=lambda p: str(p.relative_to(RAIZ / "modulos"))
)
def test_exemplo_executa_sem_erro(exemplo: Path, tmp_path: Path) -> None:
    resultado = subprocess.run(
        [sys.executable, str(exemplo)],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=tmp_path,  # roda fora do repositório: nenhum exemplo deixa arquivos para trás
    )
    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip(), "o exemplo não imprimiu nada"
    assert list(tmp_path.iterdir()) == []
