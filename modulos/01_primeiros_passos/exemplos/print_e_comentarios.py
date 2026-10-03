"""Módulo 01 - print(), comentários e o Python como calculadora.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html
- https://docs.python.org/pt-br/3/library/functions.html#print
"""


def main() -> None:
    # Isto é um comentário: o Python ignora tudo do "#" até o fim da linha.
    print("Python", "é", "divertido")  # vários valores: separados por um espaço
    print("2026", "10", "03", sep="-")  # sep= troca o separador
    print("Sem pular linha...", end=" ")  # end= troca o final (o padrão é "\n")
    print("continuou na mesma linha.")
    print(2 + 3 * 4)  # multiplicação antes da soma: 14
    print((2 + 3) * 4)  # parênteses primeiro: 20


if __name__ == "__main__":
    main()
