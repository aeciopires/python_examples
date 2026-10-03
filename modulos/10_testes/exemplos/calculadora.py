"""Módulo 10 - o código que os testes deste módulo verificam.

Os exemplos nas docstrings (linhas com ">>>") também são testes: o módulo
doctest os executa e compara a saída. Rode:
    uv run python -m doctest -v modulos/10_testes/exemplos/calculadora.py

Os testes com pytest e unittest ficam em tests/unit/test_10_testes.py e
tests/unit/test_10_testes_unittest.py.

Fontes:
- https://docs.python.org/pt-br/3/library/doctest.html
- https://docs.pytest.org/en/stable/getting-started.html
"""


def somar(a: float, b: float) -> float:
    """Soma dois números.

    >>> somar(2, 3)
    5
    >>> somar(-1, 1)
    0
    """
    return a + b


def dividir(a: float, b: float) -> float:
    """Divide a por b; lança ZeroDivisionError com uma mensagem clara se b for 0.

    >>> dividir(10, 4)
    2.5
    >>> dividir(1, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: não é possível dividir 1 por zero
    """
    if b == 0:
        raise ZeroDivisionError(f"não é possível dividir {a} por zero")
    return a / b


def media(numeros: list[float]) -> float:
    """Média aritmética; uma lista vazia é um erro.

    >>> media([7, 8, 9])
    8.0
    """
    if not numeros:
        raise ValueError("a lista de números está vazia")
    return sum(numeros) / len(numeros)


def situacao(nota: float) -> str:
    """Regra deste exemplo: menos de 5 reprova, de 5 até menos de 7 vai para
    recuperação, 7 ou mais aprova. Os limites (5 e 7) são onde os bugs moram.
    """
    if not 0 <= nota <= 10:
        raise ValueError(f"nota fora do intervalo 0-10: {nota}")
    if nota < 5:
        return "reprovado"
    if nota < 7:
        return "recuperação"
    return "aprovado"


def main() -> None:
    print(somar(2, 3), dividir(10, 4), media([7, 8, 9]))
    print(situacao(4.9), situacao(5), situacao(7))


if __name__ == "__main__":
    main()
