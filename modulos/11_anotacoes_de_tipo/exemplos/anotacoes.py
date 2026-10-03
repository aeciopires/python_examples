"""Módulo 11 - anotações de tipo (type hints): documentação que ferramentas verificam.

O Python NÃO verifica os tipos ao executar; quem verifica é uma ferramenta
separada, como o mypy (make typecheck).

Fontes:
- https://docs.python.org/pt-br/3/library/typing.html
- https://peps.python.org/pep-0484/
- https://mypy.readthedocs.io/en/stable/getting_started.html
- https://docs.python.org/pt-br/3/library/annotationlib.html
"""

import annotationlib
from collections.abc import Iterable
from typing import TypedDict


def dobro(numero: int) -> int:
    """``numero: int`` anota o parâmetro; ``-> int`` anota o retorno."""
    return numero * 2


def buscar_usuario(usuarios: dict[int, str], codigo: int) -> str | None:
    """``str | None``: devolve um texto OU None (quando o código não existe)."""
    return usuarios.get(codigo)


def total(precos: Iterable[float]) -> float:
    """Iterable aceita qualquer coisa que um for consegue percorrer (lista, tupla, ...)."""
    return sum(precos)


class Aluno(TypedDict):
    """Um dicionário com chaves e tipos conhecidos."""

    nome: str
    notas: list[float]


def media_do_aluno(aluno: Aluno) -> float:
    return sum(aluno["notas"]) / len(aluno["notas"])


def main() -> None:
    print(dobro(21))
    usuarios = {1: "ana", 2: "bia"}
    print(buscar_usuario(usuarios, 1), buscar_usuario(usuarios, 99))
    print(total([10.0, 5.5]), total((1, 2, 3)))
    print(media_do_aluno({"nome": "Caio", "notas": [6.0, 8.0]}))

    # As anotações não mudam a execução: isto RODA (e dá "abab"),
    # mas o mypy aponta o erro antes - veja o README deste módulo.
    print(dobro("ab"))  # type: ignore[arg-type]  # de propósito
    print(annotationlib.get_annotations(dobro))  # as anotações ficam guardadas na função


if __name__ == "__main__":
    main()
