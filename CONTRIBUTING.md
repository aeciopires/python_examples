<!-- TOC -->

- [Contribuindo](#contribuindo)
  - [Regras básicas](#regras-básicas)
  - [Fluxo de desenvolvimento](#fluxo-de-desenvolvimento)
  - [Alterando um exemplo](#alterando-um-exemplo)
  - [Adicionando um módulo](#adicionando-um-módulo)
  - [Diagramas](#diagramas)
  - [Atualizando versões](#atualizando-versões)
  - [Abrindo um pull request](#abrindo-um-pull-request)
  - [Reportando problemas](#reportando-problemas)

<!-- TOC -->

# Contribuindo

Obrigado pelo interesse! Esta é uma trilha de Python para iniciantes, em
português do Brasil. Contribuições de qualquer tamanho são bem-vindas: um
erro de digitação, uma explicação mais clara, uma analogia melhor, um
exercício novo, um teste que faltava ou um módulo novo.

## Regras básicas

1. **Não invente nada.** Todo fato sobre a linguagem, a biblioteca padrão
   ou as ferramentas vem de uma **fonte oficial consultada** (a
   documentação do Python, uma PEP, a documentação do pytest, do uv, do
   mise...), citada no README ou na docstring - veja
   [`CLAUDE.md`, seção 4](CLAUDE.md#4-não-invente-nada-o-guardrail-principal).
2. **Toda saída mostrada foi gerada rodando o código.** Saídas de exemplos,
   mensagens de erro e comandos de terminal são copiados de uma execução
   real, nunca escritos "de cabeça".
3. **pt-BR** em todo o texto, comentários, nomes de funções e variáveis
   (sem acentos nos identificadores: `funcoes_basicas.py`, `eh_primo`).
4. **Para iniciantes**: frases curtas, um conceito por vez, uma analogia
   para cada ideia difícil, e nenhum termo usado antes de ser explicado (ou
   com o aviso "explicado no módulo NN").
5. **Siga o contrato do módulo** - [`CLAUDE.md`, seção 3](CLAUDE.md#3-o-contrato-do-módulo).

## Fluxo de desenvolvimento

```bash
make check                                    # sistema e ferramentas
make setup                                    # mise install + uv sync
uv run python modulos/NN_tema/exemplos/x.py   # rode o que você mudou
make test-module MODULO=NN                    # os testes do módulo
make all                                      # lint, tipos, docs, doctest, cobertura e todos os exemplos
```

Os alvos do `make` são atalhos; a documentação sempre mostra também a
forma longa (`uv run ...`) - veja
[`REQUIREMENTS.md`, seção 5](REQUIREMENTS.md#5-atalhos-do-make). Como os
testes funcionam: [`docs/TESTES.md`](docs/TESTES.md).

## Alterando um exemplo

1. Altere o arquivo em `modulos/NN_tema/exemplos/`.
2. Rode-o e **copie a saída real** para o README do módulo.
3. Atualize o teste em `tests/unit/test_NN_tema.py` que compara a saída.
4. Quebre o exemplo de propósito e confira que o teste falha; desfaça.
5. `make all`.

## Adicionando um módulo

1. Leia o [`CLAUDE.md`](CLAUDE.md) e um módulo existente inteiro (README,
   exemplos e teste) - o [módulo 04](modulos/04_funcoes/README.md) é uma
   boa referência.
2. Crie `modulos/NN_tema/` com o **próximo número livre** (nunca renumere
   módulos existentes), com `README.md` e `exemplos/`.
3. Consulte as fontes oficiais de tudo o que vai ensinar.
4. Escreva os exemplos (formato em
   [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md#o-formato-de-um-exemplo)) e
   rode-os.
5. Escreva `tests/unit/test_NN_tema.py`.
6. Escreva o README com as seções do contrato e rode `make docs-fix` para
   gerar o sumário.
7. Atualize [`docs/TRILHA.md`](docs/TRILHA.md), a tabela de módulos do
   [`README.md`](README.md), o [`docs/GLOSSARIO.md`](docs/GLOSSARIO.md) (termos
   novos), o [`docs/SOLUCAO-DE-PROBLEMAS.md`](docs/SOLUCAO-DE-PROBLEMAS.md)
   (erros novos) e o [`CHANGELOG.md`](CHANGELOG.md), na seção "Não lançado".
8. `make all`.

## Diagramas

Os diagramas são **Mermaid** (blocos ` ```mermaid `), que o GitHub
renderiza - não há arquivos de imagem para manter em sincronia. As regras
estão em [`CLAUDE.md`, seção 8](CLAUDE.md#8-convenções-de-markdown). Antes
de fazer commit, renderize cada diagrama novo ou alterado para pegar erros
de sintaxe e layouts ilegíveis (precisa do Node.js; o `npx` baixa o
[mermaid-cli](https://github.com/mermaid-js/mermaid-cli) na primeira vez):

```bash
npx -p @mermaid-js/mermaid-cli mmdc -i diagrama.mmd -o diagrama.svg
```

## Atualizando versões

- **Python**: confira o [calendário oficial](https://devguide.python.org/versions/),
  altere `.python-version`, `mise.toml`, `requires-python` e as seções
  `[tool.ruff]`/`[tool.mypy]` do `pyproject.toml`, rode `make all` e
  **atualize as saídas** que mudarem (mensagens de erro mudam entre
  versões).
- **Pacotes de desenvolvimento**: `uv lock --upgrade`, depois `make all`.
- Registre a mudança no [`CHANGELOG.md`](CHANGELOG.md).

## Abrindo um pull request

1. Crie uma branch a partir da `master`: `git checkout -b <seu-nome>/<assunto>`.
2. Faça as mudanças e rode `make all` - tudo precisa passar.
3. Descreva **o que** mudou, **por quê** e **quais fontes** você consultou.
4. Atualize o `CHANGELOG.md`.
5. Antes de começar, rode `git pull origin master` para partir da versão
   mais nova e evitar conflitos.

## Reportando problemas

Abra uma [issue](https://github.com/aeciopires/python_examples/issues) com:
o módulo e o arquivo, o comando que você rodou, a saída completa (de
`make check` também, se for um problema de ambiente) e o que você esperava.
Uma explicação confusa também é um problema - se você não entendeu, conte
onde travou.
