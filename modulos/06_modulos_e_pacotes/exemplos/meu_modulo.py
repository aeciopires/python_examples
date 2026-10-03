"""Módulo 06 - um módulo é só um arquivo .py que outro arquivo pode importar.

Este arquivo é importado por usa_meu_modulo.py. Rode os dois e compare o
valor de __name__ em cada caso.

Fonte: https://docs.python.org/pt-br/3/tutorial/modules.html
"""

SAUDACAO = "Olá do meu_modulo!"  # uma "constante" (por convenção, nome em MAIÚSCULAS)


def dobro(numero: int) -> int:
    return numero * 2


def main() -> None:
    # Executado diretamente, __name__ vale "__main__".
    print(f"meu_modulo executado diretamente: __name__ = {__name__!r}")
    print(dobro(21))


# Este if impede que main() rode quando o arquivo é IMPORTADO.
if __name__ == "__main__":
    main()
