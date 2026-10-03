"""Módulo 06 - importando de um pacote (pasta geometria/).

Fonte: https://docs.python.org/pt-br/3/tutorial/modules.html#packages
"""

from geometria import formas
from geometria.formas import area_quadrado


def main() -> None:
    print(f"Área do círculo de raio 2: {formas.area_circulo(2):.2f}")
    print("Área do quadrado de lado 3:", area_quadrado(3))


if __name__ == "__main__":
    main()
