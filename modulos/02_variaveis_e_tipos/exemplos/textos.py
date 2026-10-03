"""Módulo 02 - textos (str): f-strings, índices, fatias e métodos.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html#text
- https://docs.python.org/pt-br/3/tutorial/inputoutput.html#formatted-string-literals
- https://docs.python.org/pt-br/3/library/stdtypes.html#string-methods
"""


def saudacao(nome: str) -> str:
    """Remove espaços das pontas, põe o nome em formato de título e saúda.

    >>> saudacao("  ada lovelace ")
    'Olá, Ada Lovelace!'
    """
    return f"Olá, {nome.strip().title()}!"


def main() -> None:
    linguagem = "Python"
    print(len(linguagem))  # quantidade de caracteres -> 6
    print(linguagem[0], linguagem[-1])  # primeiro e último caractere -> P n
    print(linguagem[0:2], linguagem[2:])  # fatias: [início:fim), o fim não entra -> Py thon
    print(linguagem.upper(), linguagem.lower())  # PYTHON python
    print("th" in linguagem)  # o trecho existe no texto? -> True

    versao = 3.14
    print(f"{linguagem} {versao} é a versão usada nesta trilha.")  # f-string: valores dentro de {}
    print(f"Pi com 2 casas: {3.14159:.2f}")  # formatação dentro da f-string

    frase = "banana,maçã,uva"
    frutas = frase.split(",")  # quebra o texto em uma lista
    print(frutas)
    print(" | ".join(frutas))  # junta a lista de volta em um texto
    print(frase.replace("uva", "kiwi"))  # devolve um NOVO texto: str é imutável
    print(saudacao("  ada lovelace "))


if __name__ == "__main__":
    main()
