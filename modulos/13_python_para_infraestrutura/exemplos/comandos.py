"""Módulo 13 - executando comandos externos com subprocess, com segurança.

Um script de infraestrutura vive chamando outros programas (git, docker,
kubectl, terraform...). Aqui o "programa externo" é o próprio Python
(``sys.executable``), para que o exemplo funcione em qualquer máquina.

Fontes:
- https://docs.python.org/pt-br/3/library/subprocess.html#subprocess.run
- https://docs.python.org/pt-br/3/library/subprocess.html#security-considerations
- https://docs.python.org/pt-br/3/library/shlex.html
- https://docs.python.org/pt-br/3/library/shutil.html#shutil.which
- https://docs.python.org/pt-br/3/library/sys.html#sys.executable
"""

import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class Resultado:
    """O que interessa de um comando que terminou."""

    codigo: int  # código de saída: 0 = sucesso, outro valor = falha
    saida: str  # o que o comando escreveu em stdout
    erro: str  # o que o comando escreveu em stderr


def executar(comando: list[str], tempo_limite: float = 10) -> Resultado:
    """Executa ``comando`` (uma LISTA, sem shell) e devolve o resultado, mesmo se falhar."""
    concluido = subprocess.run(
        comando,
        capture_output=True,  # guarda stdout e stderr em vez de mostrá-los no terminal
        text=True,  # devolve str em vez de bytes
        timeout=tempo_limite,  # segundos; se passar disso: TimeoutExpired
        check=False,  # não levanta exceção se o código de saída for diferente de 0
    )
    return Resultado(concluido.returncode, concluido.stdout.strip(), concluido.stderr.strip())


def executar_ou_falhar(comando: list[str], tempo_limite: float = 10) -> str:
    """Executa ``comando``; levanta CalledProcessError se o código de saída não for 0."""
    concluido = subprocess.run(
        comando, capture_output=True, text=True, timeout=tempo_limite, check=True
    )
    return concluido.stdout.strip()


def separar_comando(linha: str) -> list[str]:
    """Quebra uma linha de comando em partes, respeitando aspas, como um shell Unix faria."""
    return shlex.split(linha)


def montar_linha(partes: list[str]) -> str:
    """O inverso de separar_comando: junta as partes protegendo cada uma com aspas se preciso."""
    return shlex.join(partes)


def ferramenta_disponivel(nome: str) -> bool:
    """True se ``nome`` é um executável encontrado no PATH (ou um caminho executável)."""
    return shutil.which(nome) is not None


def main() -> None:
    python = sys.executable  # o caminho do Python que está rodando este arquivo

    ok = executar([python, "-c", "print('servidor ok')"])
    print(f"código {ok.codigo}, saída: {ok.saida!r}")

    falha = executar(
        [python, "-c", "import sys; print('disco cheio', file=sys.stderr); sys.exit(3)"]
    )
    print(f"código {falha.codigo}, erro: {falha.erro!r}")

    try:
        executar_ou_falhar([python, "-c", "import sys; sys.exit(2)"])
    except subprocess.CalledProcessError as erro:
        print("CalledProcessError, código de saída:", erro.returncode)

    try:
        executar([python, "-c", "import time; time.sleep(5)"], tempo_limite=0.5)
    except subprocess.TimeoutExpired as erro:
        print(f"TimeoutExpired depois de {erro.timeout} s")

    print(separar_comando("kubectl get pods --namespace 'meu app'"))
    print(montar_linha(["ls", "-l", "arquivo; rm -rf ~"]))  # o ";" fica preso entre aspas

    print("python encontrado?", ferramenta_disponivel(python))
    print("comando-que-nao-existe encontrado?", ferramenta_disponivel("comando-que-nao-existe"))


if __name__ == "__main__":
    main()
