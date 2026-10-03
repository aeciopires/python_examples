"""Módulo 02 - variáveis: nomes (etiquetas) que apontam para valores.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html
- https://docs.python.org/pt-br/3/library/functions.html#type
"""


def main() -> None:
    nome = "Ana"  # str (texto)
    idade = 30  # int (número inteiro)
    altura = 1.65  # float (número com casas decimais - use ponto, não vírgula)
    estudante = True  # bool (verdadeiro/falso)
    print(nome, idade, altura, estudante)

    idade = idade + 1  # reatribuição: a etiqueta "idade" agora aponta para 31
    print("Ano que vem:", idade)

    x, y = 10, 20  # atribuição múltipla
    x, y = y, x  # troca os valores sem variável auxiliar
    print("x =", x, "e y =", y)

    # type() mostra o tipo do valor para o qual a variável aponta
    print(type(nome), type(idade), type(altura), type(estudante))


if __name__ == "__main__":
    main()
