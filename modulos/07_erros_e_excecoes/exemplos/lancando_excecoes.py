"""Módulo 07 - lançando (raise) exceções e criando as suas.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/errors.html#raising-exceptions
- https://docs.python.org/pt-br/3/tutorial/errors.html#user-defined-exceptions
"""


class SaldoInsuficienteError(Exception):
    """Exceção própria: herda de Exception (classes e herança: módulo 09).

    Por convenção, o nome de uma exceção termina em "Error".
    """


def sacar(saldo: float, valor: float) -> float:
    """Devolve o novo saldo, ou lança uma exceção se o saque for inválido."""
    if valor <= 0:
        raise ValueError(f"o valor do saque deve ser positivo, recebi {valor}")
    if valor > saldo:
        raise SaldoInsuficienteError(f"saldo {saldo:.2f} é menor que o saque {valor:.2f}")
    return saldo - valor


def main() -> None:
    print(sacar(100, 30))
    for valor in (-5, 500):
        try:
            sacar(100, valor)
        except (ValueError, SaldoInsuficienteError) as erro:
            print(f"{type(erro).__name__}: {erro}")


if __name__ == "__main__":
    main()
