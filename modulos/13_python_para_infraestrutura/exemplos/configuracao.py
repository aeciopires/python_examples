"""Módulo 13 - configuração em camadas: valores padrão, arquivo TOML e variáveis de ambiente.

A regra deste exemplo: um valor da variável de ambiente vence o do arquivo,
que vence o valor padrão. Assim o mesmo programa roda em "dev" e em
"producao" mudando só o ambiente, sem editar o código.

Fontes:
- https://docs.python.org/pt-br/3/library/os.html#os.environ
- https://docs.python.org/pt-br/3/library/os.html#os.getenv
- https://docs.python.org/pt-br/3/library/tomllib.html
- https://docs.python.org/pt-br/3/library/dataclasses.html
"""

import os
import tempfile
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PREFIXO = "APP_"  # só as variáveis de ambiente que começam com isto são lidas

PADRAO: dict[str, object] = {"ambiente": "dev", "porta": 8080, "replicas": 1}


class ConfiguracaoInvalida(Exception):
    """Uma configuração ausente ou com valor errado."""


@dataclass
class Configuracao:
    ambiente: str
    porta: int
    replicas: int


def carregar_toml(caminho: Path) -> dict[str, object]:
    """Lê um arquivo TOML. O tomllib exige o arquivo aberto em modo BINÁRIO ("rb")."""
    with open(caminho, "rb") as arquivo:
        return tomllib.load(arquivo)


def ler_do_ambiente(ambiente: Mapping[str, str], prefixo: str = PREFIXO) -> dict[str, str]:
    """Pega as variáveis com o prefixo: {"APP_PORTA": "9000"} -> {"porta": "9000"}."""
    return {
        nome.removeprefix(prefixo).lower(): valor
        for nome, valor in ambiente.items()
        if nome.startswith(prefixo)
    }


def para_inteiro(nome: str, valor: object) -> int:
    """Converte para int com uma mensagem que diz QUAL configuração está errada."""
    try:
        return int(str(valor))
    except ValueError:
        raise ConfiguracaoInvalida(f"{nome} deve ser um número inteiro, recebi {valor!r}") from None


def montar_configuracao(
    padrao: Mapping[str, object],
    arquivo: Mapping[str, object],
    ambiente: Mapping[str, str],
) -> Configuracao:
    """Junta as três camadas; a da direita vence: padrão < arquivo < ambiente."""
    valores = {**padrao, **arquivo, **ler_do_ambiente(ambiente)}
    configuracao = Configuracao(
        ambiente=str(valores["ambiente"]),
        porta=para_inteiro("porta", valores["porta"]),
        replicas=para_inteiro("replicas", valores["replicas"]),
    )
    if not 1 <= configuracao.porta <= 65535:
        raise ConfiguracaoInvalida(f"porta fora do intervalo 1-65535: {configuracao.porta}")
    return configuracao


def obrigatoria(ambiente: Mapping[str, str], nome: str) -> str:
    """Devolve uma variável de ambiente que PRECISA existir (ex.: o endereço do banco)."""
    valor = ambiente.get(nome)
    if not valor:
        raise ConfiguracaoInvalida(f"variável de ambiente obrigatória ausente: {nome}")
    return valor


def mascarar(segredo: str, visiveis: int = 4) -> str:
    """Esconde um segredo para poder registrá-lo em log: só os últimos caracteres aparecem."""
    if len(segredo) <= visiveis:
        return "*" * len(segredo)
    return "*" * (len(segredo) - visiveis) + segredo[-visiveis:]


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta_temporaria:
        caminho = Path(pasta_temporaria) / "app.toml"
        caminho.write_text('ambiente = "homologacao"\nreplicas = 2\n', encoding="utf-8")
        arquivo = carregar_toml(caminho)
    print("do arquivo:", arquivo)

    # Um dicionário no lugar de os.environ, para a saída ser sempre a mesma.
    ambiente_simulado = {"APP_REPLICAS": "3", "HOME": "/home/ana"}
    print("do ambiente:", ler_do_ambiente(ambiente_simulado))
    print(montar_configuracao(PADRAO, arquivo, ambiente_simulado))
    print(montar_configuracao(PADRAO, {}, {}))  # só os valores padrão

    try:
        montar_configuracao(PADRAO, {}, {"APP_PORTA": "oitenta"})
    except ConfiguracaoInvalida as erro:
        print("ConfiguracaoInvalida:", erro)
    try:
        obrigatoria(ambiente_simulado, "APP_URL_BANCO")
    except ConfiguracaoInvalida as erro:
        print("ConfiguracaoInvalida:", erro)

    # Com o os.environ de verdade: getenv devolve o padrão quando a variável não existe.
    print(os.getenv("APP_VARIAVEL_QUE_NAO_EXISTE", "valor padrão"))
    print(mascarar("token-super-secreto-1234"))


if __name__ == "__main__":
    main()
