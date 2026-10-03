"""Módulo 04 - funções são valores: lambda, sorted(key=...), map e filter.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#lambda-expressions
- https://docs.python.org/pt-br/3/howto/sorting.html#key-functions
- https://docs.python.org/pt-br/3/library/functions.html#map
- https://docs.python.org/pt-br/3/library/functions.html#filter
"""

from collections.abc import Callable


# Callable[[int], int] significa "uma função que recebe um int e devolve um int"
# (anotações de tipo: módulo 11).
def aplicar_duas_vezes(funcao: Callable[[int], int], valor: int) -> int:
    """Recebe uma FUNÇÃO como argumento e a chama duas vezes."""
    return funcao(funcao(valor))


def dobrar(numero: int) -> int:
    return numero * 2


def main() -> None:
    print(aplicar_duas_vezes(dobrar, 5))  # dobrar(dobrar(5)) = 20

    # lambda: uma função pequena, sem nome, de uma única expressão
    print(aplicar_duas_vezes(lambda n: n + 10, 5))  # (5 + 10) + 10 = 25

    nomes = ["bia", "Carlos", "ana", "Duda"]
    print(sorted(nomes))  # maiúsculas vêm antes das minúsculas na ordem padrão
    print(sorted(nomes, key=str.lower))  # ordena ignorando maiúsculas/minúsculas
    print(sorted(nomes, key=len))  # ordena pelo tamanho

    numeros = [1, 2, 3, 4, 5, 6]
    print(list(map(dobrar, numeros)))  # aplica dobrar a cada item
    print(list(filter(lambda n: n % 2 == 0, numeros)))  # mantém só os pares


if __name__ == "__main__":
    main()
