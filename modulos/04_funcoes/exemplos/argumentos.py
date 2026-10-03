"""Módulo 04 - argumentos posicionais, nomeados, *args, **kwargs e uma armadilha.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#keyword-arguments
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#arbitrary-argument-lists
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#default-argument-values
  (o "Aviso importante" sobre valores padrão mutáveis)
"""


def descrever_pet(nome: str, especie: str = "cachorro", idade: int = 1) -> str:
    return f"{nome} é um(a) {especie} de {idade} ano(s)"


def somar(*numeros: float) -> float:
    """``*numeros`` junta QUALQUER quantidade de argumentos posicionais em uma tupla."""
    total = 0.0
    for numero in numeros:
        total += numero
    return total


def ficha(**dados: str) -> str:
    """``**dados`` junta argumentos nomeados extras em um dicionário."""
    linhas = []
    for chave, valor in dados.items():
        linhas.append(f"{chave}: {valor}")
    return "; ".join(linhas)


# ARMADILHA: o valor padrão é criado UMA vez, quando a função é definida.
# A mesma lista é reaproveitada entre as chamadas.
def adicionar_errado(item: str, lista: list[str] = []) -> list[str]:  # noqa: B006 (de propósito)
    lista.append(item)
    return lista


# Forma correta: use None como padrão e crie a lista dentro da função.
def adicionar_certo(item: str, lista: list[str] | None = None) -> list[str]:
    if lista is None:
        lista = []
    lista.append(item)
    return lista


def main() -> None:
    print(descrever_pet("Rex"))  # só o obrigatório
    print(descrever_pet("Mimi", "gato"))  # posicional: pela ordem
    print(descrever_pet("Mimi", idade=3, especie="gato"))  # nomeado: a ordem não importa
    print(somar(1, 2, 3), somar(10, 0.5), somar())
    print(ficha(nome="Ana", cidade="Recife"))

    print(adicionar_errado("a"), adicionar_errado("b"))  # ['a', 'b'] ['a', 'b'] - surpresa!
    print(adicionar_certo("a"), adicionar_certo("b"))  # ['a'] ['b']


if __name__ == "__main__":
    main()
