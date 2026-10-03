"""Módulo 05 - listas: sequências ordenadas e mutáveis.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/introduction.html#lists
- https://docs.python.org/pt-br/3/tutorial/datastructures.html#more-on-lists
- https://docs.python.org/pt-br/3/library/copy.html
"""


def main() -> None:
    compras = ["arroz", "feijão", "café"]
    print(compras[0], compras[-1])  # primeiro e último
    compras.append("leite")  # adiciona no fim
    compras.insert(0, "pão")  # adiciona na posição 0
    print(compras)
    compras.remove("feijão")  # remove pelo valor
    ultimo = compras.pop()  # remove e devolve o último
    print(ultimo, compras)
    print(len(compras), "café" in compras)

    notas = [7, 10, 5, 8]
    print(sorted(notas))  # devolve uma NOVA lista ordenada
    print(notas)  # a original continua igual
    notas.sort(reverse=True)  # ordena a PRÓPRIA lista, em ordem decrescente
    print(notas)
    print(notas[1:3])  # fatia, como em textos

    # Atribuir NÃO copia: as duas variáveis são etiquetas na MESMA lista.
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(a)  # [1, 2, 3, 4] - "a" também mudou!
    c = a.copy()  # agora sim, uma cópia (rasa)
    c.append(5)
    print(a, c)


if __name__ == "__main__":
    main()
