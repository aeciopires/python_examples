"""Módulo 09 - dataclasses: classes para guardar dados, com menos código.

Fonte: https://docs.python.org/pt-br/3/library/dataclasses.html
"""

from dataclasses import dataclass, field


@dataclass
class Produto:
    # O decorador @dataclass gera __init__, __repr__ e __eq__ a partir destes campos.
    nome: str
    preco: float
    quantidade: int = 0

    def total(self) -> float:
        return self.preco * self.quantidade


@dataclass(frozen=True)
class Ponto:
    """frozen=True: os campos não podem ser alterados depois de criados."""

    x: int
    y: int


@dataclass
class Carrinho:
    # Para valores padrão mutáveis (como listas), use field(default_factory=...)
    # - é a mesma armadilha do módulo 04.
    itens: list[Produto] = field(default_factory=list)

    def valor_total(self) -> float:
        return sum(item.total() for item in self.itens)


def main() -> None:
    cafe = Produto("Café", 18.5, 2)
    print(cafe)  # __repr__ gerado automaticamente
    print(cafe == Produto("Café", 18.5, 2))  # __eq__ compara os campos -> True
    carrinho = Carrinho()
    carrinho.itens.append(cafe)
    carrinho.itens.append(Produto("Pão", 0.75, 10))
    print(f"Total: R$ {carrinho.valor_total():.2f}")

    origem = Ponto(0, 0)
    try:
        origem.x = 5  # type: ignore[misc]  # de propósito: Ponto é frozen
    except AttributeError as erro:
        print(type(erro).__name__, "-", erro)


if __name__ == "__main__":
    main()
