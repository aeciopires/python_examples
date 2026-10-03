"""Módulo 09 - classes: o "molde" e os objetos criados a partir dele.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/classes.html#a-first-look-at-classes
- https://docs.python.org/pt-br/3/tutorial/classes.html#class-and-instance-variables
- https://docs.python.org/pt-br/3/reference/datamodel.html#object.__str__
"""


class ContaBancaria:
    """Uma conta com titular e saldo."""

    banco = "Banco Exemplo"  # atributo de CLASSE: compartilhado por todas as contas

    def __init__(self, titular: str, saldo: float = 0.0) -> None:
        # __init__ roda ao criar o objeto; self é o próprio objeto sendo criado.
        self.titular = titular  # atributos de INSTÂNCIA: cada conta tem os seus
        self.saldo = saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("o depósito deve ser positivo")
        self.saldo += valor

    def sacar(self, valor: float) -> bool:
        """Devolve True se o saque foi feito."""
        if valor > self.saldo:
            return False
        self.saldo -= valor
        return True

    def __str__(self) -> str:
        # Usado por print() e str(): um texto amigável para pessoas.
        return f"Conta de {self.titular}: R$ {self.saldo:.2f}"

    def __repr__(self) -> str:
        # Usado no REPL e em listas: um texto útil para quem programa.
        return f"ContaBancaria({self.titular!r}, {self.saldo!r})"


def main() -> None:
    conta_ana = ContaBancaria("Ana", 100)  # cria um objeto (uma instância)
    conta_bia = ContaBancaria("Bia")
    conta_ana.depositar(50)
    print(conta_ana.sacar(500), conta_ana.sacar(20))  # False True
    print(conta_ana)
    print(conta_bia)
    print([conta_ana, conta_bia])  # listas mostram o __repr__ de cada item
    print(conta_ana.banco, conta_bia.banco)
    print(isinstance(conta_ana, ContaBancaria))


if __name__ == "__main__":
    main()
