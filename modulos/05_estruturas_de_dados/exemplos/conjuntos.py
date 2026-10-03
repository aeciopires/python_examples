"""Módulo 05 - conjuntos (set): itens únicos, sem ordem, e operações de conjunto.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/datastructures.html#sets
- https://docs.python.org/pt-br/3/library/stdtypes.html#set-types-set-frozenset
"""


def remover_duplicados(itens: list[str]) -> list[str]:
    """Remove repetições e devolve em ordem alfabética (o set não guarda ordem)."""
    return sorted(set(itens))


def main() -> None:
    print(remover_duplicados(["uva", "maçã", "uva", "kiwi", "maçã"]))

    python = {"ana", "bia", "caio"}
    java = {"bia", "duda"}
    print(sorted(python | java))  # união: está em pelo menos um
    print(sorted(python & java))  # interseção: está nos dois
    print(sorted(python - java))  # diferença: está em python mas não em java
    print("ana" in python)  # testar pertencimento: um dos usos comuns de set


if __name__ == "__main__":
    main()
