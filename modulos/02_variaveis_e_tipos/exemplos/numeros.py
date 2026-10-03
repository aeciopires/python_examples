"""Módulo 02 - números inteiros (int) e de ponto flutuante (float).

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html#numbers
- https://docs.python.org/pt-br/3/library/stdtypes.html#numeric-types-int-float-complex
- https://docs.python.org/pt-br/3/tutorial/floatingpoint.html
"""


def media(a: float, b: float) -> float:
    """Devolve a média de dois números."""
    return (a + b) / 2


def main() -> None:
    print(7 / 2)  # divisão: o resultado é sempre float -> 3.5
    print(7 // 2)  # divisão inteira (arredonda para baixo) -> 3
    print(7 % 2)  # resto da divisão -> 1
    print(-7 // 2)  # "para baixo" é na direção de -infinito -> -4
    print(2**10)  # potência -> 1024
    print(2**100)  # int não tem limite fixo de tamanho
    print(0.1 + 0.2)  # float é uma aproximação binária -> 0.30000000000000004
    print(round(0.1 + 0.2, 2))  # arredonda para 2 casas -> 0.3
    print(media(7, 8))  # 7.5


if __name__ == "__main__":
    main()
