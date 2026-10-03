"""Testes do módulo 03 - decisões, laços, match e o jogo de adivinhação."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from tests._helpers import carregar_exemplo

M = "03_controle_de_fluxo"


@pytest.mark.parametrize(
    ("graus", "esperado"),
    [(-5, "frio"), (14.9, "frio"), (15, "agradável"), (24.9, "agradável"), (25, "quente")],
)
def test_classificar_temperatura(graus: float, esperado: str) -> None:
    assert carregar_exemplo(M, "condicionais").classificar_temperatura(graus) == esperado


def test_condicionais(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "condicionais").splitlines() == [
        "10°C: frio",
        "20°C: agradável",
        "30°C: quente",
        "É adulto? False",
        "17 é par? False",
        "Entre 18 e 64? False",
        "Pode entrar? False",
        "Tem algum? True",
        "Sem documento? True",
    ]


def test_funcoes_de_lacos() -> None:
    lacos = carregar_exemplo(M, "lacos")
    assert lacos.soma_ate(100) == 5050
    assert lacos.soma_ate(0) == 0
    assert lacos.contagem_regressiva(3) == [3, 2, 1]
    assert [n for n in range(20) if lacos.eh_primo(n)] == [2, 3, 5, 7, 11, 13, 17, 19]


def test_lacos(saida_de: Callable[[str, str], str]) -> None:
    linhas = saida_de(M, "lacos").splitlines()
    assert linhas[:7] == [
        "Fruta: maçã",
        "Fruta: banana",
        "Fruta: uva",
        "1 vermelho",
        "2 verde",
        "Soma de 1 a 100: 5050",
        "Contagem: [5, 4, 3, 2, 1]",
    ]
    assert linhas[7:11] == ["Ímpar: 1", "Ímpar: 3", "Ímpar: 5", "Ímpar: 7"]
    assert linhas[-1] == "9 é igual a 3 * 3"


def test_match_case(saida_de: Callable[[str, str], str]) -> None:
    assert saida_de(M, "match_case").splitlines() == [
        "200 -> OK",
        "403 -> Acesso negado",
        "404 -> Não encontrado",
        "418 -> Outro status",
        "(0, 0) -> Na origem",
        "(0, 5) -> No eixo Y, em y=5",
        "(3, 0) -> No eixo X, em x=3",
        "(2, 7) -> Em x=2, y=7",
    ]


def test_status_400() -> None:
    assert carregar_exemplo(M, "match_case").descrever_status_http(400) == "Requisição inválida"


def test_adivinhe_acerta_na_terceira(capsys: pytest.CaptureFixture[str]) -> None:
    adivinhe = carregar_exemplo(M, "adivinhe")
    palpites = iter(["1", "25", "13"])  # um "teclado de mentira"
    assert adivinhe.jogar(13, ler=lambda _pergunta: next(palpites)) == 3
    assert capsys.readouterr().out.splitlines() == [
        "Muito baixo.",
        "Muito alto.",
        "Acertou em 3 tentativa(s)!",
    ]


def test_adivinhe_erra_todas(capsys: pytest.CaptureFixture[str]) -> None:
    adivinhe = carregar_exemplo(M, "adivinhe")
    assert adivinhe.jogar(7, ler=lambda _pergunta: "1", max_tentativas=2) is None
    assert capsys.readouterr().out.splitlines()[-1] == "Não foi dessa vez. O número era 7."


def test_adivinhe_main_sem_teclado(monkeypatch: pytest.MonkeyPatch) -> None:
    adivinhe = carregar_exemplo(M, "adivinhe")

    def sem_entrada(_pergunta: str) -> str:
        raise EOFError

    # Troca o input() de verdade por um que simula "não há teclado" (EOF),
    # só durante este teste. main() deve tratar o EOFError e não quebrar.
    monkeypatch.setattr("builtins.input", sem_entrada)
    adivinhe.main()
