"""Módulo 13 - tentar de novo com espera crescente (backoff exponencial).

Na nuvem, falhas passageiras são normais: um serviço reiniciando, uma
conexão que caiu. Em vez de desistir na primeira falha (ou de tentar de
novo sem parar), o script espera um pouco, depois o dobro, depois o
dobro de novo... até um número máximo de tentativas.

Fontes:
- https://docs.python.org/pt-br/3/library/time.html#time.sleep
- https://docs.python.org/pt-br/3/library/exceptions.html#ConnectionError
- https://docs.python.org/pt-br/3/library/typing.html#generics (a sintaxe ``def f[T]``)
"""

import time
from collections.abc import Callable


def calcular_esperas(
    tentativas: int, espera_inicial: float, fator: float = 2.0, espera_maxima: float = 30.0
) -> list[float]:
    """As esperas entre as tentativas: inicial, inicial*fator, inicial*fator², ... até o máximo.

    Entre N tentativas há N-1 esperas.
    """
    if tentativas < 1:
        raise ValueError(f"tentativas deve ser pelo menos 1, recebi {tentativas}")
    return [min(espera_inicial * fator**n, espera_maxima) for n in range(tentativas - 1)]


def tentar_com_backoff[T](
    operacao: Callable[[], T],
    tentativas: int = 3,
    espera_inicial: float = 1.0,
    erros: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
    dormir: Callable[[float], None] = time.sleep,
) -> T:
    """Chama ``operacao`` até dar certo. Só tenta de novo para os ``erros`` passageiros.

    Se todas as tentativas falharem, levanta a última exceção. ``dormir`` é
    um parâmetro para que os testes não precisem esperar de verdade.
    """
    esperas = calcular_esperas(tentativas, espera_inicial)
    for numero, espera in enumerate(esperas, start=1):  # todas as tentativas, menos a última
        try:
            return operacao()
        except erros as erro:
            print(f"tentativa {numero} falhou ({erro}); nova tentativa em {espera} s")
            dormir(espera)
    return operacao()  # a última: se falhar, a exceção sobe para quem chamou


class ServicoInstavel:
    """Simula um serviço que falha nas primeiras ``falhas`` chamadas e depois responde."""

    def __init__(self, falhas: int) -> None:
        self.falhas = falhas
        self.chamadas = 0

    def consultar(self) -> str:
        self.chamadas += 1
        if self.chamadas <= self.falhas:
            raise ConnectionError("serviço indisponível")
        return "200 OK"


def main() -> None:
    print("esperas:", calcular_esperas(6, espera_inicial=1.0, espera_maxima=10.0))

    servico = ServicoInstavel(falhas=2)
    resposta = tentar_com_backoff(servico.consultar, tentativas=4, espera_inicial=0.01)
    print(f"resposta: {resposta} depois de {servico.chamadas} chamadas")

    fora_do_ar = ServicoInstavel(falhas=99)
    try:
        tentar_com_backoff(fora_do_ar.consultar, tentativas=3, espera_inicial=0.01)
    except ConnectionError as erro:
        print(f"desistindo depois de {fora_do_ar.chamadas} chamadas: {erro}")


if __name__ == "__main__":
    main()
