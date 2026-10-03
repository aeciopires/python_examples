"""Módulo 06 - três formas de importar o mesmo módulo.

Execute a partir da raiz do repositório:
    uv run python modulos/06_modulos_e_pacotes/exemplos/usa_meu_modulo.py

O Python encontra meu_modulo.py porque a pasta do script executado entra
automaticamente no caminho de busca (sys.path).

Fontes:
- https://docs.python.org/pt-br/3/tutorial/modules.html#more-on-modules
- https://docs.python.org/pt-br/3/tutorial/modules.html#the-module-search-path
"""

import meu_modulo  # importa o módulo inteiro: use meu_modulo.nome
import meu_modulo as mm  # importa com um apelido
from meu_modulo import dobro  # importa só um nome


def main() -> None:
    print(meu_modulo.SAUDACAO)
    print(mm.dobro(5), dobro(7))
    print("__name__ do módulo importado:", repr(meu_modulo.__name__))
    print("__name__ deste script:", repr(__name__))


if __name__ == "__main__":
    main()
