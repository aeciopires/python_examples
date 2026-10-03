"""Verifica (e opcionalmente corrige) a documentação Markdown do repositório.

Para cada arquivo ``.md`` (fora de ``.venv`` e de ``learning_python``):

1. O sumário entre os marcadores ``<!-- TOC -->`` deve listar exatamente os
   títulos do arquivo (``#``, ``##`` e ``###``), com âncoras no padrão do
   GitHub - veja CLAUDE.md, seção 8.
2. Todo link relativo (``../outro.md#secao``) deve apontar para um arquivo
   que existe e, se tiver ``#``, para um título que existe nesse arquivo.

Uso:
    uv run python scripts/verificar_docs.py            # só verifica (make docs)
    uv run python scripts/verificar_docs.py --corrigir # reescreve os sumários

Fontes:
- https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links
- https://docs.python.org/pt-br/3/library/re.html
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = {".venv", "learning_python", "htmlcov", ".pytest_cache", "node_modules"}
MARCADOR = "<!-- TOC -->"
TITULO = re.compile(r"^(#{1,3}) (.+?)\s*$")
CERCA = re.compile(r"^(```|~~~)")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def ancora(titulo: str) -> str:
    """A âncora que o GitHub gera para um título.

    Minúsculas; remove tudo que não for letra, dígito, espaço, ``-`` ou
    ``_``; espaços viram ``-``. Letras acentuadas são mantidas.

    >>> ancora("3.3 - Gerenciando versões com mise")
    '33---gerenciando-versões-com-mise'
    >>> ancora("O que é `__name__`?")
    'o-que-é-__name__'
    """
    texto = titulo.strip().lower()
    texto = re.sub(r"[^\w\- ]", "", texto)
    return texto.replace(" ", "-")


def titulos(texto: str) -> list[tuple[int, str]]:
    """Os títulos (nível, texto) fora de blocos de código."""
    encontrados = []
    dentro_de_codigo = False
    for linha in texto.splitlines():
        if CERCA.match(linha):
            dentro_de_codigo = not dentro_de_codigo
            continue
        if dentro_de_codigo:
            continue
        casou = TITULO.match(linha)
        if casou:
            encontrados.append((len(casou.group(1)), casou.group(2)))
    return encontrados


def ancoras(texto: str) -> set[str]:
    """Todas as âncoras do arquivo, com os sufixos -1, -2... de títulos repetidos."""
    vistas: dict[str, int] = {}
    resultado = set()
    for _, titulo in titulos(texto):
        base = ancora(titulo)
        repeticoes = vistas.get(base, 0)
        resultado.add(base if repeticoes == 0 else f"{base}-{repeticoes}")
        vistas[base] = repeticoes + 1
    return resultado


def gerar_sumario(texto: str) -> str:
    """O sumário: um item por título, recuado dois espaços por nível."""
    linhas = []
    vistas: dict[str, int] = {}
    for nivel, titulo in titulos(texto):
        base = ancora(titulo)
        repeticoes = vistas.get(base, 0)
        alvo = base if repeticoes == 0 else f"{base}-{repeticoes}"
        vistas[base] = repeticoes + 1
        rotulo = titulo.replace("[", "\\[").replace("]", "\\]")
        linhas.append(f"{'  ' * (nivel - 1)}- [{rotulo}](#{alvo})")
    return "\n".join(linhas)


def com_sumario(texto: str) -> str:
    """Devolve o texto com o sumário entre os marcadores regenerado."""
    if texto.count(MARCADOR) != 2:
        return texto
    inicio = texto.index(MARCADOR) + len(MARCADOR)
    fim = texto.index(MARCADOR, inicio)
    return f"{texto[:inicio]}\n\n{gerar_sumario(texto)}\n\n{texto[fim:]}"


def links_quebrados(arquivo: Path, texto: str) -> list[str]:
    """Links relativos cujo arquivo ou âncora não existe."""
    problemas = []
    sem_codigo = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
    for destino in LINK.findall(sem_codigo):
        if re.match(r"^[a-z]+:", destino):  # https:, mailto: ...
            continue
        caminho, _, fragmento = destino.partition("#")
        alvo = (arquivo.parent / caminho).resolve() if caminho else arquivo
        if not alvo.exists():
            problemas.append(f"{destino} (arquivo não existe)")
            continue
        if fragmento and alvo.suffix == ".md":
            if fragmento not in ancoras(alvo.read_text(encoding="utf-8")):
                problemas.append(f"{destino} (âncora não existe)")
    return problemas


def arquivos_markdown(raiz: Path) -> list[Path]:
    return sorted(
        p for p in raiz.rglob("*.md") if not IGNORAR.intersection(p.relative_to(raiz).parts)
    )


def verificar(raiz: Path, corrigir: bool) -> list[str]:
    """Devolve a lista de problemas (vazia se está tudo certo)."""
    problemas = []
    for arquivo in arquivos_markdown(raiz):
        texto = arquivo.read_text(encoding="utf-8")
        nome = arquivo.relative_to(raiz)
        esperado = com_sumario(texto)
        if esperado != texto:
            if corrigir:
                arquivo.write_text(esperado, encoding="utf-8")
                texto = esperado
            else:
                problemas.append(f"{nome}: sumário desatualizado (rode com --corrigir)")
        for link in links_quebrados(arquivo, texto):
            problemas.append(f"{nome}: link quebrado {link}")
    return problemas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--corrigir", action="store_true", help="reescreve os sumários")
    parser.add_argument("--raiz", type=Path, default=RAIZ, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    problemas = verificar(args.raiz, args.corrigir)
    for problema in problemas:
        print(problema)
    total = len(arquivos_markdown(args.raiz))
    print(f"{total} arquivo(s) verificado(s), {len(problemas)} problema(s).")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
