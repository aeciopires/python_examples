"""Módulo 08 - salvando dados estruturados em JSON e CSV.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/inputoutput.html#saving-structured-data-with-json
- https://docs.python.org/pt-br/3/library/json.html
- https://docs.python.org/pt-br/3/library/csv.html (abra com newline="")
"""

import csv
import json
import tempfile
from pathlib import Path

Registro = dict[str, str]  # um "apelido" para o tipo (anotações de tipo: módulo 11)


def salvar_json(caminho: Path, dados: dict[str, object]) -> None:
    with open(caminho, "w", encoding="utf-8") as arquivo:
        # ensure_ascii=False mantém "ç" e "ã" legíveis; indent formata o arquivo
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def carregar_json(caminho: Path) -> dict[str, object]:
    with open(caminho, encoding="utf-8") as arquivo:
        dados: dict[str, object] = json.load(arquivo)
        return dados


def salvar_csv(caminho: Path, registros: list[Registro]) -> None:
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(registros[0]))
        escritor.writeheader()  # a primeira linha: os nomes das colunas
        escritor.writerows(registros)


def ler_csv(caminho: Path) -> list[Registro]:
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))  # cada linha vira um dicionário


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        pasta = Path(pasta_temporaria)

        config = {"tema": "escuro", "fonte": 14, "idiomas": ["pt-BR", "en-US"]}
        salvar_json(pasta / "config.json", config)
        print((pasta / "config.json").read_text(encoding="utf-8"))
        print(carregar_json(pasta / "config.json") == config)

        alunos = [{"nome": "Ana", "nota": "9.5"}, {"nome": "João", "nota": "7.0"}]
        salvar_csv(pasta / "alunos.csv", alunos)
        print((pasta / "alunos.csv").read_text(encoding="utf-8"), end="")
        for aluno in ler_csv(pasta / "alunos.csv"):
            print(aluno["nome"], float(aluno["nota"]))  # CSV guarda tudo como texto


if __name__ == "__main__":
    main()
