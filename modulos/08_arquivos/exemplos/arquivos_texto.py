"""Módulo 08 - lendo e escrevendo arquivos de texto com open() e pathlib.

Os arquivos são criados em uma pasta temporária, apagada no final, para
não deixar lixo no repositório.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files
- https://docs.python.org/pt-br/3/library/functions.html#open
- https://docs.python.org/pt-br/3/library/pathlib.html
- https://docs.python.org/pt-br/3/library/tempfile.html#tempfile.TemporaryDirectory
"""

import tempfile
from pathlib import Path


def escrever_linhas(caminho: Path, linhas: list[str]) -> None:
    # "w" = write: cria o arquivo (ou APAGA o conteúdo se ele já existir).
    # "with" fecha o arquivo automaticamente, mesmo se der erro no meio.
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")


def acrescentar_linha(caminho: Path, linha: str) -> None:
    # "a" = append: escreve no FIM, sem apagar o que já existe.
    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")


def ler_linhas(caminho: Path) -> list[str]:
    # "r" = read (o padrão). Percorrer o arquivo devolve uma linha por vez.
    with open(caminho, encoding="utf-8") as arquivo:
        return [linha.rstrip("\n") for linha in arquivo]


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        pasta = Path(pasta_temporaria)
        caminho = pasta / "tarefas.txt"  # "/" junta partes de um caminho com pathlib

        escrever_linhas(caminho, ["estudar Python", "beber água"])
        acrescentar_linha(caminho, "dormir cedo")
        print(ler_linhas(caminho))

        # pathlib também lê/escreve o arquivo inteiro de uma vez:
        nota = pasta / "nota.txt"
        nota.write_text("Acentos funcionam: ação, café, pão.\n", encoding="utf-8")
        print(nota.read_text(encoding="utf-8"), end="")
        print(nota.exists(), nota.name, nota.suffix)
        print(sorted(p.name for p in pasta.iterdir()))
    print("A pasta temporária ainda existe?", pasta.exists())


if __name__ == "__main__":
    main()
