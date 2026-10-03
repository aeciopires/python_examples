"""Módulo 05 - dicionários (dict): pares chave -> valor.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries
- https://docs.python.org/pt-br/3/library/stdtypes.html#mapping-types-dict
"""


def contar_palavras(texto: str) -> dict[str, int]:
    """Conta quantas vezes cada palavra aparece (ignorando maiúsculas)."""
    contagem: dict[str, int] = {}
    for palavra in texto.lower().split():
        contagem[palavra] = contagem.get(palavra, 0) + 1  # get: valor ou 0 se não existir
    return contagem


def main() -> None:
    pessoa = {"nome": "Ana", "idade": 30}
    print(pessoa["nome"])  # acessa pela chave
    pessoa["cidade"] = "Recife"  # cria uma chave nova
    pessoa["idade"] = 31  # altera uma chave existente
    print(pessoa)
    print(pessoa.get("email", "sem e-mail"))  # get não dá erro se a chave não existir
    del pessoa["cidade"]
    for chave, valor in pessoa.items():  # percorre os pares
        print(f"{chave} = {valor}")
    print(list(pessoa.keys()), list(pessoa.values()))
    print(contar_palavras("o rato roeu a roupa o rato"))


if __name__ == "__main__":
    main()
