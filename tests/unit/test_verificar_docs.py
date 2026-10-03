"""Testes de scripts/verificar_docs.py - o verificador de sumários e links (make docs)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from tests._helpers import RAIZ


def _carregar() -> ModuleType:
    caminho = RAIZ / "scripts" / "verificar_docs.py"
    spec = importlib.util.spec_from_file_location("verificar_docs", caminho)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["verificar_docs"] = modulo  # argparse/dataclasses esperam o módulo registrado
    spec.loader.exec_module(modulo)
    return modulo


vd = _carregar()


@pytest.mark.parametrize(
    ("titulo", "esperado"),
    [
        ("Visão geral", "visão-geral"),
        ("3.3 - Gerenciando versões com mise", "33---gerenciando-versões-com-mise"),
        ("`funcoes_basicas.py`", "funcoes_basicaspy"),
        ("Analogia: a receita e o liquidificador", "analogia-a-receita-e-o-liquidificador"),
        ("[0.2.0] - 2026-10-03", "020---2026-10-03"),
    ],
)
def test_ancora_segue_a_regra_do_github(titulo: str, esperado: str) -> None:
    assert vd.ancora(titulo) == esperado


def test_titulos_ignora_blocos_de_codigo() -> None:
    texto = "# Título\n```bash\n# comentário, não título\n```\n## Seção\n"
    assert vd.titulos(texto) == [(1, "Título"), (2, "Seção")]


def test_titulos_repetidos_ganham_sufixo() -> None:
    texto = "# A\n## Adicionado\n## Adicionado\n"
    assert vd.ancoras(texto) == {"a", "adicionado", "adicionado-1"}
    assert "(#adicionado-1)" in vd.gerar_sumario(texto)


def test_com_sumario_regenera_entre_os_marcadores() -> None:
    texto = "<!-- TOC -->\nvelho\n<!-- TOC -->\n\n# Doc\n\n## Parte [1]\n"
    novo = vd.com_sumario(texto)
    assert "velho" not in novo
    assert "- [Doc](#doc)\n  - [Parte \\[1\\]](#parte-1)" in novo
    assert vd.com_sumario(novo) == novo  # rodar de novo não muda nada


def test_sem_marcadores_nao_altera() -> None:
    assert vd.com_sumario("# Só um título\n") == "# Só um título\n"


def _repo(tmp_path: Path, conteudo: str) -> Path:
    (tmp_path / "outro.md").write_text("# Outro\n\n## Seção certa\n", encoding="utf-8")
    (tmp_path / "doc.md").write_text(conteudo, encoding="utf-8")
    return tmp_path


def test_links_validos_e_externos_passam(tmp_path: Path) -> None:
    raiz = _repo(tmp_path, "# Doc\n[a](outro.md#seção-certa) [b](https://x.org/#y) [c](#doc)\n")
    assert vd.verificar(raiz, corrigir=False) == []


def test_link_quebrado_e_ancora_inexistente(tmp_path: Path) -> None:
    raiz = _repo(tmp_path, "# Doc\n[a](nao_existe.md) [b](outro.md#errada) [c](#nada)\n")
    problemas = vd.verificar(raiz, corrigir=False)
    assert "doc.md: link quebrado nao_existe.md (arquivo não existe)" in problemas
    assert "doc.md: link quebrado outro.md#errada (âncora não existe)" in problemas
    assert "doc.md: link quebrado #nada (âncora não existe)" in problemas


def test_links_dentro_de_codigo_sao_ignorados(tmp_path: Path) -> None:
    raiz = _repo(tmp_path, "# Doc\n```text\n[a](nao_existe.md)\n```\n")
    assert vd.verificar(raiz, corrigir=False) == []


def test_sumario_desatualizado_e_corrigido(tmp_path: Path) -> None:
    raiz = _repo(tmp_path, "<!-- TOC -->\n<!-- TOC -->\n\n# Doc\n")
    assert vd.verificar(raiz, corrigir=False) == [
        "doc.md: sumário desatualizado (rode com --corrigir)"
    ]
    assert vd.verificar(raiz, corrigir=True) == []
    assert "- [Doc](#doc)" in (raiz / "doc.md").read_text(encoding="utf-8")


def test_main_codigo_de_saida(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    raiz = _repo(tmp_path, "# Doc\n[a](nao_existe.md)\n")
    assert vd.main(["--raiz", str(raiz)]) == 1
    assert "1 problema(s)" in capsys.readouterr().out
    (raiz / "doc.md").write_text("# Doc\n", encoding="utf-8")
    assert vd.main(["--raiz", str(raiz)]) == 0


def test_o_repositorio_esta_em_dia() -> None:
    assert vd.verificar(RAIZ, corrigir=False) == []
