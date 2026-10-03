"""Módulo 04 - definindo funções: def, parâmetros, return e docstrings.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#default-argument-values
- https://peps.python.org/pep-0257/ (convenções de docstrings)
"""


def area_retangulo(largura: float, altura: float) -> float:
    """Devolve a área de um retângulo.

    A primeira string dentro da função é a "docstring": a documentação que
    aparece em help(area_retangulo).
    """
    return largura * altura


def saudar(nome: str, saudacao: str = "Olá") -> str:
    """``saudacao`` tem um valor padrão: pode ser omitida na chamada."""
    return f"{saudacao}, {nome}!"


def menor_e_maior(numeros: list[int]) -> tuple[int, int]:
    """Devolve dois valores de uma vez (na verdade, uma tupla)."""
    return min(numeros), max(numeros)


def avisar(mensagem: str) -> None:
    """Uma função sem return devolve None."""
    print("Aviso:", mensagem)


def main() -> None:
    print(area_retangulo(3, 4))  # 12
    print(saudar("Ana"))  # usa o padrão
    print(saudar("Ana", "Bom dia"))  # substitui o padrão
    menor, maior = menor_e_maior([5, 2, 9, 1])  # "desempacota" a tupla
    print(menor, maior)
    retorno = avisar("disco quase cheio")  # type: ignore[func-returns-value]  # de propósito
    print("avisar() devolveu:", retorno)


if __name__ == "__main__":
    main()
