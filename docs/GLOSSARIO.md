<!-- TOC -->

- [Glossário](#glossário)
  - [Termos](#termos)
  - [Referências](#referências)

<!-- TOC -->

# Glossário

Os termos usados na trilha, em ordem alfabética, com o módulo onde
aparecem pela primeira vez. Para as definições oficiais (e muitos outros
termos), veja o [Glossário da documentação do Python](https://docs.python.org/pt-br/3/glossary.html).

## Termos

| Termo | Significado | Módulo |
|---|---|---|
| **ambiente virtual** (venv, `.venv`) | uma pasta com um Python e pacotes só deste projeto, isolada dos outros | [12](../modulos/12_ambientes_e_dependencias/README.md) |
| **anotação de tipo** (*type hint*) | `: int`, `-> str`: documenta os tipos esperados; o Python não verifica, o mypy sim | [11](../modulos/11_anotacoes_de_tipo/README.md) |
| **argumento** | o valor passado na **chamada** de uma função (`saudar("Ana")`) | [04](../modulos/04_funcoes/README.md) |
| **atributo** | um valor guardado em um objeto (`conta.saldo`) | [09](../modulos/09_classes_e_objetos/README.md) |
| **biblioteca padrão** | os módulos que já vêm com o Python (`math`, `json`, `pathlib`...) | [06](../modulos/06_modulos_e_pacotes/README.md) |
| **bytecode** | a forma intermediária para a qual o Python traduz o código antes de executar; fica em cache em `__pycache__/` | [01](../modulos/01_primeiros_passos/README.md) |
| **classe** | o "molde" que define os atributos e métodos de um tipo de objeto | [09](../modulos/09_classes_e_objetos/README.md) |
| **cobertura de testes** | quais linhas e ramos do código os testes executaram | [10](../modulos/10_testes/README.md) |
| **compreensão** (*comprehension*) | `[x * 2 for x in itens]`: cria uma lista/set/dict em uma linha | [05](../modulos/05_estruturas_de_dados/README.md) |
| **conjunto** (`set`) | coleção sem ordem e sem itens repetidos | [05](../modulos/05_estruturas_de_dados/README.md) |
| **dependência** | um pacote de que o seu projeto precisa | [12](../modulos/12_ambientes_e_dependencias/README.md) |
| **dicionário** (`dict`) | pares chave -> valor | [05](../modulos/05_estruturas_de_dados/README.md) |
| **docstring** | o texto entre `"""` logo no início de uma função, classe ou módulo; aparece em `help()` | [04](../modulos/04_funcoes/README.md) |
| **doctest** | exemplos `>>>` em uma docstring que também são executados como testes | [10](../modulos/10_testes/README.md) |
| **exceção** | um erro durante a execução, que pode ser tratado com `try`/`except` | [07](../modulos/07_erros_e_excecoes/README.md) |
| **f-string** | `f"Olá, {nome}"`: texto com valores inseridos entre `{}` | [02](../modulos/02_variaveis_e_tipos/README.md) |
| **fixture** | no pytest, algo que um teste recebe pronto pelo nome do parâmetro (`tmp_path`, `capsys`...) | [10](../modulos/10_testes/README.md) |
| **função** | um bloco de código com nome, que recebe parâmetros e devolve um resultado | [04](../modulos/04_funcoes/README.md) |
| **herança** | uma classe que reaproveita (e estende) outra: `class Tubarao(Peixe)` | [09](../modulos/09_classes_e_objetos/README.md) |
| **imutável** | que não pode ser alterado depois de criado (`str`, `int`, `tuple`) | [02](../modulos/02_variaveis_e_tipos/README.md) |
| **indentação** | o recuo no começo da linha, que define os blocos | [01](../modulos/01_primeiros_passos/README.md) |
| **instância** / **objeto** | uma "coisa" criada a partir de uma classe; em Python, todo valor é um objeto | [09](../modulos/09_classes_e_objetos/README.md) |
| **interpretador** | o programa `python`, que lê e executa o seu código | [01](../modulos/01_primeiros_passos/README.md) |
| **lambda** | uma função pequena, sem nome, de uma expressão | [04](../modulos/04_funcoes/README.md) |
| **laço** (*loop*) | repetição: `for` ou `while` | [03](../modulos/03_controle_de_fluxo/README.md) |
| **linter** | ferramenta que aponta problemas de estilo e erros prováveis sem executar o código (aqui, o ruff) | [04](../modulos/04_funcoes/README.md) |
| **lista** (`list`) | sequência ordenada e mutável | [05](../modulos/05_estruturas_de_dados/README.md) |
| **lockfile** (`uv.lock`) | o registro das versões exatas de cada dependência | [12](../modulos/12_ambientes_e_dependencias/README.md) |
| **método** | uma função que pertence a um objeto (`"ana".upper()`) | [09](../modulos/09_classes_e_objetos/README.md) |
| **módulo** | um arquivo `.py` que pode ser importado | [06](../modulos/06_modulos_e_pacotes/README.md) |
| **mutável** | que pode ser alterado depois de criado (`list`, `dict`, `set`) | [05](../modulos/05_estruturas_de_dados/README.md) |
| **`None`** | o valor que representa "nenhum valor" | [02](../modulos/02_variaveis_e_tipos/README.md) |
| **pacote** (*package*) | uma pasta de módulos com `__init__.py`; também, algo instalável do PyPI | [06](../modulos/06_modulos_e_pacotes/README.md) |
| **parâmetro** | o nome que recebe um valor na **definição** da função (`def saudar(nome)`) | [04](../modulos/04_funcoes/README.md) |
| **PEP** | *Python Enhancement Proposal*: os documentos que descrevem mudanças e convenções da linguagem (ex.: PEP 8, estilo) | [01](../modulos/01_primeiros_passos/README.md) |
| **polimorfismo** | o mesmo código funcionando com objetos de classes diferentes | [09](../modulos/09_classes_e_objetos/README.md) |
| **PyPI** | o repositório oficial de pacotes Python ([pypi.org](https://pypi.org)) | [12](../modulos/12_ambientes_e_dependencias/README.md) |
| **REPL** | o modo interativo (`>>>`): lê, executa, mostra o resultado, repete | [01](../modulos/01_primeiros_passos/README.md) |
| **traceback** | o relatório de um erro, com o caminho de chamadas até a linha que falhou | [07](../modulos/07_erros_e_excecoes/README.md) |
| **tupla** (`tuple`) | sequência ordenada e imutável | [05](../modulos/05_estruturas_de_dados/README.md) |
| **variável** | um nome (etiqueta) que aponta para um valor | [02](../modulos/02_variaveis_e_tipos/README.md) |
| **`__name__`** | o "crachá" de um módulo: `"__main__"` quando executado diretamente | [06](../modulos/06_modulos_e_pacotes/README.md) |

## Referências

- [Glossário da documentação do Python](https://docs.python.org/pt-br/3/glossary.html)
- [PEP 1 - o que é uma PEP](https://peps.python.org/pep-0001/)
