"""Módulo 05 - compreensões: criando listas, sets e dicts em uma linha.

Fonte: https://docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions
"""


def quadrados(n: int) -> list[int]:
    """[expressão for item in sequência] - o mesmo que um for com append."""
    return [x**2 for x in range(n)]


def pares(numeros: list[int]) -> list[int]:
    """Com "if" no final, a compreensão filtra os itens."""
    return [n for n in numeros if n % 2 == 0]


def main() -> None:
    # Forma longa...
    resultado = []
    for x in range(5):
        resultado.append(x**2)
    print(resultado)
    # ...e a compreensão equivalente
    print(quadrados(5))
    print(pares([1, 2, 3, 4, 5, 6]))

    palavras = ["sol", "lua", "estrela"]
    print({p: len(p) for p in palavras})  # compreensão de dicionário
    print(sorted({len(p) for p in palavras}))  # compreensão de conjunto (sem repetidos)


if __name__ == "__main__":
    main()
