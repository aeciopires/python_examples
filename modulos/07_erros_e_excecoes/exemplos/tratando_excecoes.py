"""Módulo 07 - tratando erros com try / except / else / finally.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/errors.html#handling-exceptions
- https://docs.python.org/pt-br/3/tutorial/errors.html#defining-clean-up-actions
- https://docs.python.org/pt-br/3/library/exceptions.html
"""


def ler_inteiro(texto: str) -> int | None:
    """Converte o texto para int; devolve None se o texto não for um número."""
    try:
        return int(texto)
    except ValueError:
        return None


def dividir(a: float, b: float) -> str:
    """Mostra cada parte do try em ação."""
    try:
        resultado = a / b  # pode lançar ZeroDivisionError
    except ZeroDivisionError:
        return "não dá para dividir por zero"
    else:
        # roda só se o try NÃO lançou exceção
        return f"{a} / {b} = {resultado}"
    finally:
        # roda SEMPRE, com ou sem erro (ótimo para "arrumar a casa")
        print(f"[finally] dividir({a}, {b}) terminou")


def descrever_erro(valor: object) -> str:
    """Captura vários tipos de exceção e mostra o nome de cada uma."""
    try:
        return str(10 / int(valor))  # type: ignore[call-overload]  # de propósito
    except (ValueError, TypeError) as erro:  # uma tupla captura vários tipos
        return f"{type(erro).__name__}: {erro}"
    except ZeroDivisionError as erro:
        return f"{type(erro).__name__}: {erro}"


def main() -> None:
    print(ler_inteiro("42"), ler_inteiro("quarenta e dois"))
    print(dividir(10, 2))
    print(dividir(1, 0))
    for valor in ["5", "abc", None, "0"]:
        print(repr(valor), "->", descrever_erro(valor))


if __name__ == "__main__":
    main()
