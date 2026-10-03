"""Testes do módulo 08 - arquivos. ``tmp_path`` é uma pasta temporária do pytest.

Fonte: https://docs.pytest.org/en/stable/how-to/tmp_path.html
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from tests._helpers import carregar_exemplo

M = "08_arquivos"


def test_arquivos_texto(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "arquivos_texto").splitlines() == [
        "['estudar Python', 'beber água', 'dormir cedo']",
        "Acentos funcionam: ação, café, pão.",
        "True nota.txt .txt",
        "['nota.txt', 'tarefas.txt']",
        "A pasta temporária ainda existe? False",
    ]


def test_escrever_apaga_e_acrescentar_mantem(tmp_path: Path) -> None:
    exemplo = carregar_exemplo(M, "arquivos_texto")
    caminho = tmp_path / "lista.txt"
    exemplo.escrever_linhas(caminho, ["velho"])
    exemplo.escrever_linhas(caminho, ["novo"])  # "w" apaga o conteúdo anterior
    exemplo.acrescentar_linha(caminho, "mais um")  # "a" acrescenta no fim
    assert exemplo.ler_linhas(caminho) == ["novo", "mais um"]


def test_json_ida_e_volta(tmp_path: Path) -> None:
    exemplo = carregar_exemplo(M, "json_e_csv")
    dados: dict[str, object] = {"cidade": "São Paulo", "itens": [1, 2], "ativo": True}
    exemplo.salvar_json(tmp_path / "d.json", dados)
    assert exemplo.carregar_json(tmp_path / "d.json") == dados
    assert "São Paulo" in (tmp_path / "d.json").read_text(encoding="utf-8")


def test_csv_ida_e_volta(tmp_path: Path) -> None:
    exemplo = carregar_exemplo(M, "json_e_csv")
    registros = [{"nome": "Ana", "nota": "9.5"}, {"nome": "Zé, o Bom", "nota": "6"}]
    exemplo.salvar_csv(tmp_path / "a.csv", registros)
    assert exemplo.ler_csv(tmp_path / "a.csv") == registros  # a vírgula no nome sobrevive


def test_json_e_csv(saida_de: Callable[[str, str], str]) -> None:
    linhas = saida_de(M, "json_e_csv").splitlines()
    assert linhas[0] == "{"
    assert "True" in linhas
    assert linhas[-3:] == ["João,7.0", "Ana 9.5", "João 7.0"]
