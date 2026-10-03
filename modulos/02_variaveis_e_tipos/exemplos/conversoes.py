"""Módulo 02 - convertendo entre tipos, valores "verdadeiros" e None.

Fontes:
- https://docs.python.org/pt-br/3/library/functions.html (int, float, str, bool)
- https://docs.python.org/pt-br/3/library/stdtypes.html#truth-value-testing
- https://docs.python.org/pt-br/3/library/constants.html#None
"""


def main() -> None:
    texto = "42"
    numero = int(texto)  # str -> int
    print(numero + 1)  # 43 (com o texto, "42" + 1 seria um erro)
    print(float("3.5") * 2)  # str -> float -> 7.0
    print(str(10) + "0")  # int -> str, e "+" entre textos concatena -> 100
    print(int(3.99))  # float -> int corta as casas decimais -> 3

    # bool(): zero e "vazios" são falsos; o resto é verdadeiro
    print(bool(0), bool(""), bool([]), bool(None))  # False False False False
    print(bool(7), bool("0"), bool([0]))  # True True True ("0" não é vazio!)

    resultado = None  # None representa "nenhum valor"
    print(resultado is None)  # compare com None usando "is" -> True


if __name__ == "__main__":
    main()
