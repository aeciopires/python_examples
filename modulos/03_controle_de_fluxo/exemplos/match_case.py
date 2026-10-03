"""Módulo 03 - escolhendo entre vários casos com match / case (Python 3.10+).

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#match-statements
- https://peps.python.org/pep-0636/ (tutorial do pattern matching)
"""


def descrever_status_http(status: int) -> str:
    """Traduz alguns códigos de status HTTP (exemplo adaptado do tutorial oficial)."""
    match status:
        case 200:
            return "OK"
        case 400:
            return "Requisição inválida"
        case 401 | 403:  # "|" combina vários valores em um único caso
            return "Acesso negado"
        case 404:
            return "Não encontrado"
        case _:  # "_" é o curinga: casa com qualquer valor
            return "Outro status"


def onde_esta(ponto: tuple[int, int]) -> str:
    """Desestrutura uma tupla (x, y) dentro do próprio case."""
    match ponto:
        case (0, 0):
            return "Na origem"
        case (0, y):
            return f"No eixo Y, em y={y}"
        case (x, 0):
            return f"No eixo X, em x={x}"
        case (x, y):
            return f"Em x={x}, y={y}"


def main() -> None:
    for status in (200, 403, 404, 418):
        print(status, "->", descrever_status_http(status))
    for ponto in [(0, 0), (0, 5), (3, 0), (2, 7)]:
        print(ponto, "->", onde_esta(ponto))


if __name__ == "__main__":
    main()
