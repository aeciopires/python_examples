"""Módulo 06 - a biblioteca padrão: módulos que já vêm com o Python.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/stdlib.html
- https://docs.python.org/pt-br/3/library/math.html
- https://docs.python.org/pt-br/3/library/datetime.html
- https://docs.python.org/pt-br/3/library/statistics.html
- https://docs.python.org/pt-br/3/library/collections.html#collections.Counter
"""

import math
import statistics
from collections import Counter
from datetime import date


def dias_entre(inicio: date, fim: date) -> int:
    """Subtrair duas datas dá um timedelta; .days é a diferença em dias."""
    return (fim - inicio).days


def main() -> None:
    print(math.sqrt(16), math.floor(2.7), math.ceil(2.1))
    print(f"{math.pi:.5f}")

    notas = [7.5, 8.0, 6.0, 9.5]
    print(statistics.mean(notas), statistics.median(notas))

    print(Counter("abracadabra").most_common(2))  # as 2 letras mais frequentes

    print(dias_entre(date(2026, 1, 1), date(2026, 12, 25)))
    print(date(2026, 10, 3).isoformat())


if __name__ == "__main__":
    main()
