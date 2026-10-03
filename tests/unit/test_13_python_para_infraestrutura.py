"""Testes do módulo 13 - Python para infraestrutura (DevOps e cloud).

Nenhum teste usa a rede nem espera de verdade: o "comando externo" é o
próprio Python (``sys.executable``) e as esperas do backoff são simuladas.

Fontes:
- https://docs.pytest.org/en/stable/how-to/tmp_path.html
- https://docs.pytest.org/en/stable/how-to/parametrize.html
"""

from __future__ import annotations

import io
import ipaddress
import os
import subprocess
import sys
import tomllib
from collections.abc import Callable
from pathlib import Path

import pytest

from tests._helpers import carregar_exemplo

M = "13_python_para_infraestrutura"


# --- comandos.py ------------------------------------------------------------------


def test_comandos(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "comandos").splitlines() == [
        "código 0, saída: 'servidor ok'",
        "código 3, erro: 'disco cheio'",
        "CalledProcessError, código de saída: 2",
        "TimeoutExpired depois de 0.5 s",
        "['kubectl', 'get', 'pods', '--namespace', 'meu app']",
        "ls -l 'arquivo; rm -rf ~'",
        "python encontrado? True",
        "comando-que-nao-existe encontrado? False",
    ]


def test_executar_captura_saida_e_codigo() -> None:
    comandos = carregar_exemplo(M, "comandos")
    resultado = comandos.executar([sys.executable, "-c", "print('a'); raise SystemExit(5)"])
    assert (resultado.codigo, resultado.saida, resultado.erro) == (5, "a", "")


def test_executar_ou_falhar() -> None:
    comandos = carregar_exemplo(M, "comandos")
    assert comandos.executar_ou_falhar([sys.executable, "-c", "print('ok')"]) == "ok"
    with pytest.raises(subprocess.CalledProcessError) as erro:
        comandos.executar_ou_falhar([sys.executable, "-c", "raise SystemExit(1)"])
    assert erro.value.returncode == 1


def test_tempo_limite() -> None:
    comandos = carregar_exemplo(M, "comandos")
    with pytest.raises(subprocess.TimeoutExpired):
        comandos.executar([sys.executable, "-c", "import time; time.sleep(5)"], tempo_limite=0.2)


def test_comando_inexistente() -> None:
    comandos = carregar_exemplo(M, "comandos")
    with pytest.raises(FileNotFoundError):
        comandos.executar(["comando-que-nao-existe"])


def test_shlex_ida_e_volta() -> None:
    comandos = carregar_exemplo(M, "comandos")
    partes = ["echo", "nome com espaço", "a;b", "$HOME"]
    assert comandos.separar_comando(comandos.montar_linha(partes)) == partes


# --- configuracao.py --------------------------------------------------------------


def test_configuracao(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "configuracao").splitlines() == [
        "do arquivo: {'ambiente': 'homologacao', 'replicas': 2}",
        "do ambiente: {'replicas': '3'}",
        "Configuracao(ambiente='homologacao', porta=8080, replicas=3)",
        "Configuracao(ambiente='dev', porta=8080, replicas=1)",
        "ConfiguracaoInvalida: porta deve ser um número inteiro, recebi 'oitenta'",
        "ConfiguracaoInvalida: variável de ambiente obrigatória ausente: APP_URL_BANCO",
        "valor padrão",
        "********************1234",
    ]


def test_ambiente_vence_arquivo_que_vence_padrao() -> None:
    config = carregar_exemplo(M, "configuracao")
    resultado = config.montar_configuracao(
        {"ambiente": "dev", "porta": 1, "replicas": 1},
        {"porta": 2, "replicas": 2},
        {"APP_PORTA": "3", "OUTRA_PORTA": "4"},
    )
    assert (resultado.ambiente, resultado.porta, resultado.replicas) == ("dev", 3, 2)


@pytest.mark.parametrize(
    ("porta", "valida"), [("0", False), ("1", True), ("65535", True), ("65536", False)]
)
def test_limites_da_porta(porta: str, valida: bool) -> None:
    config = carregar_exemplo(M, "configuracao")
    if valida:
        assert config.montar_configuracao(config.PADRAO, {}, {"APP_PORTA": porta}).porta == int(
            porta
        )
    else:
        with pytest.raises(config.ConfiguracaoInvalida, match="porta fora do intervalo"):
            config.montar_configuracao(config.PADRAO, {}, {"APP_PORTA": porta})


def test_variavel_obrigatoria() -> None:
    config = carregar_exemplo(M, "configuracao")
    assert config.obrigatoria({"APP_URL": "x"}, "APP_URL") == "x"
    with pytest.raises(config.ConfiguracaoInvalida):
        config.obrigatoria({"APP_URL": ""}, "APP_URL")  # vazia conta como ausente


def test_variavel_de_ambiente_de_verdade(monkeypatch: pytest.MonkeyPatch) -> None:
    config = carregar_exemplo(M, "configuracao")
    monkeypatch.setenv("APP_REPLICAS", "7")
    assert config.montar_configuracao(config.PADRAO, {}, os.environ).replicas == 7


def test_toml_exige_modo_binario_e_formato_valido(tmp_path: Path) -> None:
    config = carregar_exemplo(M, "configuracao")
    caminho = tmp_path / "ruim.toml"
    caminho.write_text("porta = \n", encoding="utf-8")
    with pytest.raises(tomllib.TOMLDecodeError):
        config.carregar_toml(caminho)


@pytest.mark.parametrize(
    ("segredo", "esperado"), [("", ""), ("abc", "***"), ("abcd", "****"), ("abcde", "*bcde")]
)
def test_mascarar(segredo: str, esperado: str) -> None:
    assert carregar_exemplo(M, "configuracao").mascarar(segredo) == esperado


# --- analisar_logs.py -------------------------------------------------------------


def test_analisar_logs(saida_de: Callable[[str, str], str]) -> None:
    aviso = "WARNING: linha 5 ignorada (formato inesperado): 'linha cortada no meio'"
    resumo = ["200: 3", "201: 1", "503: 1"]
    assert saida_de(M, "analisar_logs").splitlines() == [
        aviso,
        *resumo,
        "ERROR: taxa de erros 20% acima do limite de 5%",
        "código de saída: 1",
        aviso,
        *resumo,
        "INFO: taxa de erros 20% dentro do limite",
        "código de saída: 0",
        "ERROR: arquivo não encontrado: nao_existe.log",
        "código de saída: 1",
    ]


def test_interpretar_linha() -> None:
    logs = carregar_exemplo(M, "analisar_logs")
    requisicao = logs.interpretar_linha("2026-10-03T10:00:01 GET /api/saude 200 12ms\n")
    assert (requisicao.metodo, requisicao.rota, requisicao.status, requisicao.duracao_ms) == (
        "GET",
        "/api/saude",
        200,
        12,
    )
    assert logs.interpretar_linha("") is None
    assert logs.interpretar_linha("2026-10-03T10:00:01 GET /api 20 12ms") is None  # status curto


@pytest.mark.parametrize(
    ("status", "eh_erro"), [(499, False), (500, True), (599, True), (600, False)]
)
def test_taxa_de_erros_limites(status: int, eh_erro: bool) -> None:
    logs = carregar_exemplo(M, "analisar_logs")
    requisicao = logs.Requisicao("GET", "/", status, 1)
    assert logs.taxa_de_erros([requisicao]) == (1.0 if eh_erro else 0.0)
    assert logs.taxa_de_erros([]) == 0.0


def test_verboso_mostra_debug(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    logs = carregar_exemplo(M, "analisar_logs")
    caminho = tmp_path / "a.log"
    caminho.write_text("2026-10-03T10:00:01 GET / 200 1ms\n", encoding="utf-8")
    fluxo = io.StringIO()
    assert logs.executar([str(caminho), "--verboso"], fluxo_de_log=fluxo) == 0
    assert fluxo.getvalue().splitlines()[0].startswith("DEBUG: linha 1:")
    assert capsys.readouterr().out == "200: 1\n"


def test_logs_vao_para_stderr_por_padrao(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    logs = carregar_exemplo(M, "analisar_logs")
    assert logs.executar([str(tmp_path / "nao_existe.log")]) == 1
    capturado = capsys.readouterr()
    assert capturado.out == ""
    assert "ERROR: arquivo não encontrado" in capturado.err


def test_argumento_invalido_sai_com_codigo_2() -> None:
    logs = carregar_exemplo(M, "analisar_logs")
    with pytest.raises(SystemExit) as saida:
        logs.executar(["a.log", "--limite", "muito"], fluxo_de_log=io.StringIO())
    assert saida.value.code == 2


# --- redes.py ---------------------------------------------------------------------


def test_redes(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "redes").splitlines() == [
        "10.0.0.0/16: 65536 endereços, máscara 255.255.0.0, de 10.0.0.0 a 10.0.255.255",
        "10.0.1.0/24: 256 endereços, máscara 255.255.255.0, de 10.0.1.0 a 10.0.1.255",
        "10.0.0.0/16 em /24: 256 sub-redes; as 3 primeiras:",
        "  10.0.0.0/24",
        "  10.0.1.0/24",
        "  10.0.2.0/24",
        "em 4 partes iguais: ['10.0.0.0/18', '10.0.64.0/18', '10.0.128.0/18', '10.0.192.0/18']",
        "[('10.0.0.0/16', '10.0.128.0/17')]",
        "10.0.3.7 em 10.0.0.0/22? True",
        "10.0.4.1 em 10.0.0.0/22? False",
        "2001:db8::/64: 18446744073709551616 endereços, máscara ffff:ffff:ffff:ffff::, "
        "de 2001:db8:: a 2001:db8::ffff:ffff:ffff:ffff",
    ]


def test_dividir_limites() -> None:
    redes = carregar_exemplo(M, "redes")
    assert redes.dividir("10.0.0.0/24", 32)[-1] == ipaddress.ip_network("10.0.0.255/32")
    assert len(redes.dividir("10.0.0.0/24", 32)) == 256
    with pytest.raises(ValueError, match="new prefix must be longer"):
        redes.dividir("10.0.0.0/24", 23)


def test_sobreposicoes() -> None:
    redes = carregar_exemplo(M, "redes")
    assert redes.sobreposicoes(["10.0.0.0/24", "10.0.1.0/24"]) == []  # vizinhas, sem conflito
    assert redes.sobreposicoes(["10.0.0.0/24", "10.0.0.0/24"]) == [("10.0.0.0/24", "10.0.0.0/24")]
    assert redes.sobreposicoes(["10.0.0.0/8", "2001:db8::/32"]) == []  # IPv4 x IPv6


def test_pertence_limites() -> None:
    redes = carregar_exemplo(M, "redes")
    assert redes.pertence("10.0.0.0", "10.0.0.0/22")  # o primeiro endereço
    assert redes.pertence("10.0.3.255", "10.0.0.0/22")  # o último
    assert not redes.pertence("9.255.255.255", "10.0.0.0/22")


@pytest.mark.parametrize(
    ("cidr", "mensagem"),
    [("10.0.0.1/24", "has host bits set"), ("10.0.0.0/33", "does not appear to be")],
)
def test_rede_invalida(cidr: str, mensagem: str) -> None:
    with pytest.raises(ValueError, match=mensagem):
        carregar_exemplo(M, "redes").descrever(cidr)


# --- retentativas.py --------------------------------------------------------------


def test_retentativas(saida_de: Callable[[str, str], str]) -> None:
    falhas = [
        "tentativa 1 falhou (serviço indisponível); nova tentativa em 0.01 s",
        "tentativa 2 falhou (serviço indisponível); nova tentativa em 0.02 s",
    ]
    assert saida_de(M, "retentativas").splitlines() == [
        "esperas: [1.0, 2.0, 4.0, 8.0, 10.0]",
        *falhas,
        "resposta: 200 OK depois de 3 chamadas",
        *falhas,
        "desistindo depois de 3 chamadas: serviço indisponível",
    ]


def test_calcular_esperas_limites() -> None:
    retentativas = carregar_exemplo(M, "retentativas")
    assert retentativas.calcular_esperas(1, 1.0) == []  # uma tentativa: nenhuma espera
    assert retentativas.calcular_esperas(3, 0.5, fator=3) == [0.5, 1.5]
    with pytest.raises(ValueError, match="pelo menos 1"):
        retentativas.calcular_esperas(0, 1.0)


def test_backoff_nao_espera_de_verdade(capsys: pytest.CaptureFixture[str]) -> None:
    retentativas = carregar_exemplo(M, "retentativas")
    esperas: list[float] = []
    servico = retentativas.ServicoInstavel(falhas=3)
    resposta = retentativas.tentar_com_backoff(
        servico.consultar, tentativas=4, espera_inicial=1.0, dormir=esperas.append
    )
    assert resposta == "200 OK"
    assert esperas == [1.0, 2.0, 4.0]
    assert len(capsys.readouterr().out.splitlines()) == 3


def test_backoff_nao_repete_erros_permanentes() -> None:
    retentativas = carregar_exemplo(M, "retentativas")
    chamadas: list[int] = []

    def operacao() -> str:
        chamadas.append(1)
        raise ValueError("configuração errada")  # tentar de novo não resolveria

    with pytest.raises(ValueError):
        retentativas.tentar_com_backoff(operacao, tentativas=5, dormir=lambda _: None)
    assert len(chamadas) == 1


# --- integridade.py ---------------------------------------------------------------


def test_integridade(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "integridade").splitlines() == [
        "SHA-256 de b'': e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "checksum publicado: f20db34e4a2067852e95802cd6b2c49634f8197a508af0bdd32d09eb4a650776",
        "arquivo confere? True",
        "depois de alterado, confere? False",
    ]


def test_arquivo_confere(tmp_path: Path) -> None:
    integridade = carregar_exemplo(M, "integridade")
    caminho = tmp_path / "vazio.bin"
    caminho.write_bytes(b"")
    esperado = integridade.sha256_de_bytes(b"")
    assert integridade.arquivo_confere(caminho, esperado.upper() + "\n")  # aceita maiúsculas
    assert not integridade.arquivo_confere(caminho, "0" * 64)
    with pytest.raises(FileNotFoundError):
        integridade.sha256_de_arquivo(tmp_path / "nao_existe.bin")
