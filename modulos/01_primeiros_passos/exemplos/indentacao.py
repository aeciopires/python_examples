"""Módulo 01 - a indentação (recuo) define os blocos de código.

Em Python não há chaves { }: o que está recuado "pertence" à linha
terminada em ":" logo acima. O padrão (PEP 8) é usar 4 espaços.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html#first-steps-towards-programming
- https://peps.python.org/pep-0008/#indentation
"""


def main() -> None:
    idade = 20
    if idade >= 18:
        print("Esta linha está DENTRO do if (recuada 4 espaços).")
        print("Esta também: só rodam se a condição for verdadeira.")
    print("Esta linha está FORA do if: roda sempre.")


if __name__ == "__main__":
    main()
