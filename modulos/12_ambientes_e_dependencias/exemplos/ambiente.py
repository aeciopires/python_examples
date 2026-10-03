"""Módulo 12 - em qual Python e em qual ambiente virtual este código está rodando?

Compare a saída de:
    uv run python modulos/12_ambientes_e_dependencias/exemplos/ambiente.py
    python3 modulos/12_ambientes_e_dependencias/exemplos/ambiente.py

Fontes:
- https://docs.python.org/pt-br/3/library/venv.html (seção "Como funcionam os venvs")
- https://docs.python.org/pt-br/3/library/sys.html#sys.prefix
- https://docs.python.org/pt-br/3/library/importlib.metadata.html
"""

import platform
import sys
from importlib.metadata import PackageNotFoundError, version


def esta_em_ambiente_virtual() -> bool:
    """A documentação do venv: basta comparar sys.prefix com sys.base_prefix."""
    return sys.prefix != sys.base_prefix


def versao_do_pacote(nome: str) -> str | None:
    """Versão de um pacote instalado no ambiente atual, ou None se não estiver instalado."""
    try:
        return version(nome)
    except PackageNotFoundError:
        return None


def main() -> None:
    print("Versão do Python:", platform.python_version())
    print("Executável:", sys.executable)
    print("Em um ambiente virtual?", esta_em_ambiente_virtual())
    for pacote in ("pytest", "ruff", "pacote-que-nao-existe"):
        print(f"{pacote}: {versao_do_pacote(pacote) or 'não instalado'}")


if __name__ == "__main__":
    main()
