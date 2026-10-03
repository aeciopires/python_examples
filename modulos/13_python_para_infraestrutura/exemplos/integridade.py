"""Módulo 13 - conferindo a integridade de um arquivo com um hash SHA-256.

Antes de instalar um binário ou implantar um artefato, confira se o
arquivo baixado é exatamente o publicado: calcule o SHA-256 dele e
compare com o valor que o fornecedor divulga (o *checksum*).

Fontes:
- https://docs.python.org/pt-br/3/library/hashlib.html#hashlib.file_digest
- https://docs.python.org/pt-br/3/library/hashlib.html#hash-algorithms
"""

import hashlib
import tempfile
from pathlib import Path


def sha256_de_bytes(dados: bytes) -> str:
    """O SHA-256 de alguns bytes, em hexadecimal (64 caracteres)."""
    return hashlib.sha256(dados).hexdigest()


def sha256_de_arquivo(caminho: Path) -> str:
    """O SHA-256 de um arquivo; file_digest exige o arquivo aberto em modo binário ("rb")."""
    with open(caminho, "rb") as arquivo:
        return hashlib.file_digest(arquivo, "sha256").hexdigest()


def arquivo_confere(caminho: Path, esperado: str) -> bool:
    """True se o SHA-256 do arquivo é igual ao ``esperado`` (maiúsculas ou minúsculas)."""
    return sha256_de_arquivo(caminho) == esperado.strip().lower()


def main() -> None:
    print("SHA-256 de b'':", sha256_de_bytes(b""))

    with tempfile.TemporaryDirectory() as pasta_temporaria:
        artefato = Path(pasta_temporaria) / "app-1.0.0.tar.gz"
        artefato.write_bytes(b"conteudo do pacote, versao 1.0.0\n")
        publicado = sha256_de_arquivo(artefato)  # o valor que o "fornecedor" divulgaria
        print("checksum publicado:", publicado)
        print("arquivo confere?", arquivo_confere(artefato, publicado))

        artefato.write_bytes(b"conteudo do pacote, versao 1.0.0 (alterado)\n")
        print("depois de alterado, confere?", arquivo_confere(artefato, publicado))


if __name__ == "__main__":
    main()
