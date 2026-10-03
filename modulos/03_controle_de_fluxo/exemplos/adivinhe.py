"""Módulo 03 - jogo de adivinhação: junta if, for, break e input().

Execute em um terminal (o jogo espera você digitar):
    uv run python modulos/03_controle_de_fluxo/exemplos/adivinhe.py

Fontes:
- https://docs.python.org/pt-br/3/library/functions.html#input
- https://docs.python.org/pt-br/3/library/random.html#random.randint
"""

import random
from collections.abc import Callable


def dica(palpite: int, segredo: int) -> str:
    """Compara o palpite com o número secreto."""
    if palpite < segredo:
        return "baixo"
    if palpite > segredo:
        return "alto"
    return "acertou"


def jogar(segredo: int, ler: Callable[[str], str] = input, max_tentativas: int = 5) -> int | None:
    """Joga uma partida e devolve quantas tentativas foram usadas (None se errou todas).

    ``ler`` é a função que lê o palpite - por padrão, ``input``. Receber essa
    função como parâmetro permite testar o jogo sem teclado (docs/TESTES.md).
    """
    for tentativa in range(1, max_tentativas + 1):
        palpite = int(ler(f"Tentativa {tentativa}/{max_tentativas} - seu palpite (1 a 25): "))
        resultado = dica(palpite, segredo)
        if resultado == "acertou":
            print(f"Acertou em {tentativa} tentativa(s)!")
            return tentativa
        print(f"Muito {resultado}.")
    print(f"Não foi dessa vez. O número era {segredo}.")
    return None


def main() -> None:
    segredo = random.randint(1, 25)  # sorteia um inteiro entre 1 e 25 (inclusive)
    try:
        jogar(segredo, ler=input)
    except EOFError:  # sem teclado (ex.: make run-all) - o módulo 07 explica try/except
        print("\nSem entrada disponível: jogo encerrado.")


if __name__ == "__main__":
    main()
