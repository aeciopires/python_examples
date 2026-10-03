"""Módulo 03 - decisões com if / elif / else e operadores lógicos.

Fontes:
- https://docs.python.org/pt-br/3/tutorial/controlflow.html#if-statements
- https://docs.python.org/pt-br/3/library/stdtypes.html#boolean-operations-and-or-not
- https://docs.python.org/pt-br/3/library/stdtypes.html#comparisons
"""


def classificar_temperatura(graus: float) -> str:
    """Classifica uma temperatura em graus Celsius.

    O Python testa as condições de cima para baixo e executa só o PRIMEIRO
    bloco cuja condição for verdadeira.
    """
    if graus < 15:
        return "frio"
    elif graus < 25:
        return "agradável"
    else:
        return "quente"


def eh_adulto(idade: int) -> bool:
    """A regra deste exemplo: 18 anos ou mais."""
    return idade >= 18


def eh_par(numero: int) -> bool:
    """Um número é par quando o resto da divisão por 2 é zero."""
    return numero % 2 == 0


def main() -> None:
    for graus in (10, 20, 30):
        print(f"{graus}°C: {classificar_temperatura(graus)}")

    idade = 17
    print("É adulto?", eh_adulto(idade))
    print("17 é par?", eh_par(17))

    # Comparações encadeadas: 18 <= idade < 65 é o mesmo que
    # (18 <= idade) and (idade < 65)
    print("Entre 18 e 64?", 18 <= idade < 65)

    tem_ingresso = True
    tem_documento = False
    print("Pode entrar?", tem_ingresso and tem_documento)  # and: os dois precisam ser True
    print("Tem algum?", tem_ingresso or tem_documento)  # or: basta um ser True
    print("Sem documento?", not tem_documento)  # not: inverte


if __name__ == "__main__":
    main()
