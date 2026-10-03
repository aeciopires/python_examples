"""Módulo 05 - tuplas: sequências imutáveis e desempacotamento.

Fonte: https://docs.python.org/pt-br/3/tutorial/datastructures.html#tuples-and-sequences
"""


def main() -> None:
    ponto = (3, 4)  # uma tupla: não pode ser alterada depois de criada
    x, y = ponto  # desempacotamento
    print(x, y)

    unico = (42,)  # tupla de UM item precisa da vírgula
    nao_tupla = 42  # sem vírgula, (42) seria só o número 42 entre parênteses
    print(type(unico), type(nao_tupla))

    data = (2026, 10, 3)
    ano, mes, dia = data
    print(f"{dia:02d}/{mes:02d}/{ano}")  # :02d = inteiro com 2 dígitos, completando com zero

    try:
        ponto[0] = 10  # type: ignore[index]  # de propósito: tuplas são imutáveis
    except TypeError as erro:
        print("Erro:", erro)


if __name__ == "__main__":
    main()
