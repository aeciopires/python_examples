"""Módulo 13 - uma ferramenta de linha de comando que analisa um log de acesso.

Junta o que um script de operação costuma ter: argumentos (argparse),
mensagens de log (logging), expressões regulares (re), contagem (Counter)
e um código de saída que diz ao pipeline se deu certo (0) ou não (1).

O formato das linhas é a regra deste exemplo (não é um padrão real):
    2026-10-03T10:00:01 GET /api/saude 200 12ms

Fontes:
- https://docs.python.org/pt-br/3/library/argparse.html
- https://docs.python.org/pt-br/3/howto/logging.html
- https://docs.python.org/pt-br/3/library/logging.handlers.html#streamhandler
- https://docs.python.org/pt-br/3/library/re.html
- https://docs.python.org/pt-br/3/library/collections.html#collections.Counter
- https://docs.python.org/pt-br/3/library/sys.html#sys.exit (0 = sucesso)
"""

import argparse
import logging
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

PADRAO_LINHA = re.compile(
    r"^(?P<data>\S+) (?P<metodo>[A-Z]+) (?P<rota>\S+) (?P<status>\d{3}) (?P<duracao>\d+)ms$"
)


@dataclass
class Requisicao:
    metodo: str
    rota: str
    status: int
    duracao_ms: int


def interpretar_linha(linha: str) -> Requisicao | None:
    """Transforma uma linha em Requisicao, ou None se ela não seguir o formato."""
    encontrado = PADRAO_LINHA.match(linha.strip())
    if encontrado is None:
        return None
    return Requisicao(
        metodo=encontrado["metodo"],
        rota=encontrado["rota"],
        status=int(encontrado["status"]),
        duracao_ms=int(encontrado["duracao"]),
    )


def contar_status(requisicoes: list[Requisicao]) -> Counter[int]:
    """Quantas vezes cada código de status HTTP apareceu."""
    return Counter(requisicao.status for requisicao in requisicoes)


def taxa_de_erros(requisicoes: list[Requisicao]) -> float:
    """Fração (0.0 a 1.0) das requisições com status 500 a 599; 0.0 se não houver nenhuma."""
    if not requisicoes:
        return 0.0
    erros = sum(1 for requisicao in requisicoes if 500 <= requisicao.status <= 599)
    return erros / len(requisicoes)


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="analisar_logs", description="Resume um log de acesso e checa a taxa de erros."
    )
    parser.add_argument("arquivo", type=Path, help="o arquivo de log")
    parser.add_argument(
        "--limite", type=float, default=0.05, help="taxa de erros máxima aceita (padrão: 0.05)"
    )
    parser.add_argument("--verboso", action="store_true", help="mostra também mensagens DEBUG")
    return parser


def configurar_logger(verboso: bool, fluxo: TextIO) -> logging.Logger:
    """Um logger só desta ferramenta, escrevendo em ``fluxo``."""
    logger = logging.getLogger("analisar_logs")
    logger.handlers.clear()  # evita mensagens repetidas se a função for chamada de novo
    manipulador = logging.StreamHandler(fluxo)
    manipulador.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(manipulador)
    logger.setLevel(logging.DEBUG if verboso else logging.INFO)
    logger.propagate = False
    return logger


def executar(argv: list[str], fluxo_de_log: TextIO | None = None) -> int:
    """Roda a ferramenta e devolve o código de saída: 0 = saudável, 1 = problema."""
    argumentos = criar_parser().parse_args(argv)
    logger = configurar_logger(argumentos.verboso, fluxo_de_log or sys.stderr)

    try:
        linhas = argumentos.arquivo.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        logger.error("arquivo não encontrado: %s", argumentos.arquivo)
        return 1

    requisicoes = []
    for numero, linha in enumerate(linhas, start=1):
        requisicao = interpretar_linha(linha)
        if requisicao is None:
            logger.warning("linha %d ignorada (formato inesperado): %r", numero, linha)
        else:
            logger.debug("linha %d: %s", numero, requisicao)
            requisicoes.append(requisicao)

    for status, quantidade in sorted(contar_status(requisicoes).items()):
        print(f"{status}: {quantidade}")
    taxa = taxa_de_erros(requisicoes)
    if taxa > argumentos.limite:
        logger.error(
            "taxa de erros %.0f%% acima do limite de %.0f%%", taxa * 100, argumentos.limite * 100
        )
        return 1
    logger.info("taxa de erros %.0f%% dentro do limite", taxa * 100)
    return 0


LOG_DE_EXEMPLO = """\
2026-10-03T10:00:01 GET /api/saude 200 12ms
2026-10-03T10:00:02 GET /api/pedidos 200 85ms
2026-10-03T10:00:03 POST /api/pedidos 201 140ms
2026-10-03T10:00:04 GET /api/pedidos 503 3001ms
linha cortada no meio
2026-10-03T10:00:05 GET /api/saude 200 9ms
"""


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        caminho = Path(pasta_temporaria) / "acesso.log"
        caminho.write_text(LOG_DE_EXEMPLO, encoding="utf-8")

        # Os logs vão para sys.stdout só para aparecerem aqui; o padrão é stderr.
        codigo = executar([str(caminho)], fluxo_de_log=sys.stdout)
        print("código de saída:", codigo)
        codigo = executar([str(caminho), "--limite", "0.25"], fluxo_de_log=sys.stdout)
        print("código de saída:", codigo)
    codigo = executar(["nao_existe.log"], fluxo_de_log=sys.stdout)
    print("código de saída:", codigo)


if __name__ == "__main__":
    main()
