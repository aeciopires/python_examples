"""Módulo 03 - repetições com for e while, break, continue e else.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#for-statements
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#the-range-function
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#break-and-continue-statements
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#else-clauses-on-loops
- https://docs.python.org/pt-br/3/library/functions.html#enumerate
"""


def soma_ate(n: int) -> int:
    """Soma 1 + 2 + ... + n usando for e range()."""
    total = 0
    for numero in range(1, n + 1):  # range(1, n + 1) vai de 1 até n (o fim não entra)
        total += numero  # o mesmo que: total = total + numero
    return total


def contagem_regressiva(inicio: int) -> list[int]:
    """Conta de ``inicio`` até 1 usando while."""
    numeros = []
    while inicio > 0:  # repete ENQUANTO a condição for verdadeira
        numeros.append(inicio)
        inicio -= 1  # sem esta linha o laço nunca terminaria
    return numeros


def eh_primo(n: int) -> bool:
    """Um primo só é divisível por 1 e por ele mesmo (exemplo do tutorial oficial)."""
    if n < 2:
        return False
    for divisor in range(2, n):
        if n % divisor == 0:
            return False
    return True


def main() -> None:
    for fruta in ["maçã", "banana", "uva"]:  # percorre cada item da lista
        print("Fruta:", fruta)

    for posicao, cor in enumerate(["vermelho", "verde"], start=1):  # posição + item
        print(posicao, cor)

    print("Soma de 1 a 100:", soma_ate(100))
    print("Contagem:", contagem_regressiva(5))

    for numero in range(10):
        if numero % 2 == 0:
            continue  # pula o resto desta volta e vai para o próximo número
        if numero > 7:
            break  # sai do laço imediatamente
        print("Ímpar:", numero)

    # O "else" de um for roda quando o laço termina SEM break.
    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, "é igual a", x, "*", n // x)
                break
        else:
            print(n, "é um número primo")


if __name__ == "__main__":
    main()
