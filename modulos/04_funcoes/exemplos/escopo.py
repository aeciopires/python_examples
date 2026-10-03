"""Módulo 04 - escopo: onde um nome "existe" (local, global e a regra LEGB).

Fontes:
- https://docs.python.org/pt-br/3/tutorial/classes.html#python-scopes-and-namespaces
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions
- https://docs.python.org/pt-br/3/reference/simple_stmts.html#the-global-statement
"""

from collections.abc import Callable

mensagem = "global"  # definida fora de qualquer função: escopo global do módulo
contador = 0


def mostrar() -> str:
    # Não existe "mensagem" local; o Python procura no escopo de fora (global).
    return mensagem


def sombrear() -> str:
    mensagem = "local"  # cria uma variável LOCAL que esconde (sombreia) a global
    return mensagem


def incrementar() -> int:
    global contador  # sem isto, "contador += 1" daria UnboundLocalError
    contador += 1
    return contador


# Callable[[int], int] significa "uma função que recebe um int e devolve um int"
# (anotações de tipo: módulo 11).
def criar_multiplicador(fator: int) -> Callable[[int], int]:
    """Uma função dentro de outra "lembra" das variáveis de fora (escopo Enclosing)."""

    def multiplicar(numero: int) -> int:
        return numero * fator

    return multiplicar


def main() -> None:
    print(mostrar())  # global
    print(sombrear())  # local
    print(mensagem)  # global (a função não alterou a global)
    print(incrementar(), incrementar())  # 1 2
    triplicar = criar_multiplicador(3)
    print(triplicar(5))  # 15


if __name__ == "__main__":
    main()
