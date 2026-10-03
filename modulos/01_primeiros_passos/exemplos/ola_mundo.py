"""Módulo 01 - o primeiro programa: mostrar um texto na tela.

Execute com:
    uv run python modulos/01_primeiros_passos/exemplos/ola_mundo.py

Fonte: https://docs.python.org/pt-br/3/tutorial/introduction.html
"""


def main() -> None:
    print("Olá, mundo!")


# Ponto de partida: só roda quando o arquivo é executado diretamente.
# O módulo 06 explica a linha abaixo em detalhes.
if __name__ == "__main__":
    main()
