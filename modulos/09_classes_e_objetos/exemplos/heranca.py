"""Módulo 09 - herança e polimorfismo.

Versão revisada dos exemplos de peixes de learning_python/fish.py.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/classes.html#inheritance
- https://docs.python.org/pt-br/3/library/functions.html#super
"""


class Peixe:
    def __init__(self, nome: str, esqueleto: str = "ósseo") -> None:
        self.nome = nome
        self.esqueleto = esqueleto

    def nadar(self) -> str:
        return f"{self.nome} está nadando."

    def nadar_de_re(self) -> str:
        return f"{self.nome} consegue nadar de ré."


class PeixePalhaco(Peixe):
    """Herda tudo de Peixe e ACRESCENTA um método."""

    def morar_na_anemona(self) -> str:
        return f"{self.nome} vive entre as anêmonas."


class Tubarao(Peixe):
    """Herda de Peixe e SOBRESCREVE (override) partes dele."""

    def __init__(self, nome: str) -> None:
        super().__init__(nome, esqueleto="cartilaginoso")  # reaproveita o __init__ da mãe

    def nadar_de_re(self) -> str:
        return f"{self.nome} não nada de ré, mas consegue afundar de ré."


def main() -> None:
    nemo = PeixePalhaco("Nemo")
    bruce = Tubarao("Bruce")
    print(nemo.morar_na_anemona())
    print(nemo.esqueleto, "|", bruce.esqueleto)

    # Polimorfismo: o mesmo código funciona com objetos de classes diferentes;
    # cada um responde do seu jeito.
    for peixe in (nemo, bruce):
        print(peixe.nadar(), peixe.nadar_de_re())

    print(isinstance(bruce, Peixe), issubclass(Tubarao, Peixe))  # True True


if __name__ == "__main__":
    main()
