<!-- TOC -->
<!-- TOC -->

# CLAUDE.md

Guia para quem mantém ou amplia este repositório - pessoas ou assistentes
de programação com IA, como o Claude Code. Leia antes de adicionar ou
editar um módulo.

## 1. Sobre este repositório

`python_examples` é uma trilha **pública e para iniciantes** de
programação em Python 3, escrita em **português do Brasil (pt-BR)**. São 13
módulos (`modulos/NN_tema/`), cada um com um README (explicação,
analogias, diagramas Mermaid, saídas reais, erros comuns, exercícios e
referências), exemplos executáveis em `exemplos/` e um arquivo de testes em
`tests/unit/`. Os exemplos usam **só a biblioteca padrão**; as ferramentas
são o [uv](https://docs.astral.sh/uv/) (dependências e ambiente virtual), o
[mise](https://mise.jdx.dev) (versões do Python e do uv) e o `make`
(atalhos). Funciona em Ubuntu, macOS e Windows com WSL2
([`REQUIREMENTS.md`, seção 1](REQUIREMENTS.md#1-sistemas-operacionais-suportados)).

A pasta `learning_python/` guarda exemplos antigos, em inglês, mantidos por
histórico: fora da trilha, do lint, dos tipos e dos testes. Não a altere
sem um pedido explícito.

Toda a documentação é **pt-BR**.

## 2. Estrutura de diretórios e arquivos

```text
.
├── README.md               # página inicial: o que é, início rápido, módulos
├── LICENSE                 # GPL-3.0 - não altere sem um pedido
├── REQUIREMENTS.md         # sistemas suportados, hardware, instalação, mise, uv, make
├── CONTRIBUTING.md         # como propor uma mudança ou um módulo
├── CHANGELOG.md            # no estilo Keep a Changelog
├── CLAUDE.md               # este arquivo
├── pyproject.toml          # dependências de desenvolvimento e configuração de pytest, coverage, ruff, mypy
├── uv.lock                 # gerado pelo uv - nunca edite à mão
├── .python-version         # 3.14 (lido pelo uv)
├── mise.toml               # python 3.14 e uv (lido pelo mise)
├── Makefile                # atalhos - REQUIREMENTS.md, seção 5
├── scripts/
│   ├── check-deps.sh       # make check
│   └── verificar_docs.py   # make docs / make docs-fix: sumários e links dos .md
├── docs/
│   ├── TRILHA.md               # os módulos em fases
│   ├── ARQUITETURA.md          # como tudo se encaixa (diagramas)
│   ├── TESTES.md               # como os testes funcionam
│   ├── SOLUCAO-DE-PROBLEMAS.md # sintoma -> causa -> solução
│   └── GLOSSARIO.md            # termos da trilha
├── modulos/
│   └── NN_tema/            # README.md + exemplos/*.py - seção 3
├── tests/
│   ├── conftest.py         # fixture saida_de
│   ├── _helpers.py         # carregar_exemplo(), todos_os_exemplos()
│   └── unit/
│       ├── test_NN_tema.py              # um por módulo - obrigatório
│       ├── test_exemplos_executam.py    # todo exemplo roda sem erro
│       └── test_verificar_docs.py
└── learning_python/        # legado (en-US) - não faz parte da trilha
```

**Um módulo novo recebe o próximo número livre** e entra em
[`docs/TRILHA.md`](docs/TRILHA.md); módulos existentes nunca são
renumerados.

## 3. O contrato do módulo

Todo `modulos/NN_tema/` tem:

1. **`exemplos/*.py`**, cada um com:
   - uma docstring no topo dizendo o que mostra e as **fontes oficiais**
     usadas (URLs);
   - funções pequenas, com anotações de tipo, testáveis uma a uma;
   - `def main() -> None:` que demonstra tudo com `print()`;
   - `if __name__ == "__main__": main()` no fim;
   - **só a biblioteca padrão**, sem rede, sem deixar arquivos para trás
     (use `tempfile`), e terminando sem erro mesmo **sem teclado**
     (`< /dev/null`), porque `make run-all` e
     `tests/unit/test_exemplos_executam.py` rodam assim.
2. **`README.md`** com estas seções, nesta ordem (pode acrescentar seções
   explicativas depois de "Conceitos" ou "Exemplos"): Visão geral (com o
   pré-requisito), O que você vai aprender, Analogia(s), Conceitos (com
   pelo menos um diagrama Mermaid), Exemplos (para cada arquivo: o comando
   `uv run python ...` e a **saída real**), Testes, Erros comuns (com as
   **mensagens reais** do Python), Exercícios, Referências.
3. **`tests/unit/test_NN_tema.py`** (mesmo número) que:
   - compara a saída de cada `main()` com a do README (fixture `saida_de`);
   - testa as funções diretamente, incluindo **limites** e **erros**
     (`pytest.raises`);
   - falha quando o exemplo é quebrado de propósito.
4. **Cobertura: nunca abaixo de 80%** (`make coverage`); hoje está perto
   de 100% - mantenha o código novo coberto.

## 4. Não invente nada: o guardrail principal

1. **Todo fato sobre a linguagem, a biblioteca padrão, as ferramentas e os
   comandos vem de uma fonte consultada de verdade** - a
   [documentação do Python em pt-BR](https://docs.python.org/pt-br/3/)
   (tutorial, referência da biblioteca, glossário), as
   [PEPs](https://peps.python.org/), ou a documentação oficial da
   ferramenta (pytest, uv, mise, ruff, mypy, GNU make). Não a memória.
   Prefira a versão pt-BR da documentação do Python quando ela existir.
2. **Verifique rodando.** Toda saída de exemplo, mensagem de erro, saída de
   comando e sessão de terminal em um README foi copiada de uma execução
   real, com a versão do Python fixada. Quando uma saída depende da máquina
   (caminhos, versões, tempos), diga isso no texto.
3. **Citações** da documentação são literais e com link; ao parafrasear,
   não acrescente o que a fonte não diz.
4. **Números e versões são o conteúdo mais arriscado** (versões do Python e
   dos pacotes, datas de suporte, tamanhos): confira na fonte atual, diga a
   data da consulta e que podem mudar.
5. **Analogias** simplificam, mas não podem contradizer o comportamento
   real; quando uma analogia tiver limite, diga onde (veja o "bytecode" no
   módulo 01).
6. **Exemplos neutros**: evite regras jurídicas, médicas ou financeiras
   reais (idade para votar, faixas de IMC...) - use regras declaradas como
   "a regra deste exemplo".
7. Se uma página não abrir, tente outra URL oficial; se algo continuar sem
   verificação, deixe de fora ou diga explicitamente que não foi verificado.
8. Antes de publicar uma URL com âncora (`#secao`), confirme que a âncora
   existe na página.

## 5. Idioma e público

- Texto, comentários, docstrings, mensagens impressas, nomes de funções,
  variáveis e arquivos em **pt-BR**. Identificadores **sem acento**
  (`eh_primo`, `funcoes_basicas.py`); textos e comentários **com** acento.
- Termos técnicos em inglês aparecem entre parênteses ou em itálico na
  primeira vez (*type hint*, *traceback*) e entram no
  [`docs/GLOSSARIO.md`](docs/GLOSSARIO.md).
- Mensagens de erro do Python ficam **no original** (em inglês), porque é
  assim que a pessoa vai vê-las no terminal; a explicação vem em pt-BR.
- O leitor é **iniciante**: um conceito por vez, frases curtas, nenhum
  termo usado antes de ser explicado (ou com "explicado no módulo NN").

## 6. Convenções de Python

- Python **3.14**, fixado em `.python-version`, `mise.toml` e
  `requires-python`.
- `make lint` (ruff, regras E, W, F, I, UP, B; linhas até 100 caracteres)
  e `make typecheck` (mypy com `disallow_untyped_defs`) passam sem erros.
- Erros **propositais** (para ensinar) levam o comentário mais específico
  possível, com o motivo: `# noqa: B006 (de propósito)`,
  `# type: ignore[arg-type]  # de propósito`.
- Testes usam `from __future__ import annotations` e anotações de tipo.
- Tudo roda via `uv run` (nunca `pip install` ou o Python do sistema).

## 7. Ferramentas: mise, uv e make

- **mise** fixa `python` e `uv` em [`mise.toml`](mise.toml); o uv também lê
  [`.python-version`](.python-version) - mantenha os dois iguais.
- **uv** gerencia as dependências de desenvolvimento (grupo `dev` do
  [`pyproject.toml`](pyproject.toml)) e o `uv.lock` (sempre versionado).
  Os exemplos **não** têm dependências de runtime (`dependencies = []`).
- **make**: cada alvo é um atalho para comandos documentados por extenso.
  Nunca substitua um comando longo da documentação por um alvo do make -
  mostre os dois. Escreva o `Makefile` compatível com o GNU make 3.81 (o do
  macOS) e o `scripts/check-deps.sh` compatível com o bash 3.2.
- `scripts/check-deps.sh` e a tabela da
  [`REQUIREMENTS.md`, seção 3](REQUIREMENTS.md#3-software-necessário) ficam
  em sincronia.

## 8. Convenções de Markdown

- Um sumário entre marcadores `<!-- TOC -->` no topo de todo arquivo,
  **gerado** por `make docs-fix` (não edite à mão) e verificado por
  `make docs`.
- Âncoras seguem a regra do GitHub: minúsculas; remove tudo que não for
  letra (acentuadas incluídas), dígito, espaço, `-` ou `_`; espaços viram
  `-`. O `make docs` acusa links relativos quebrados e âncoras inexistentes.
- Somente links relativos entre arquivos do repositório
  (`../../REQUIREMENTS.md#3-software-necessário`).
- Tabelas para comparações; todo README termina com `## Referências` (só
  fontes oficiais).
- **Diagramas são Mermaid** (blocos ` ```mermaid `, que o GitHub renderiza) -
  nenhum arquivo de imagem para manter em sincronia. Use só `flowchart`,
  `sequenceDiagram` ou `stateDiagram-v2`; rótulos entre aspas duplas,
  `<br/>` para quebrar linha, `{placeholder}` em vez de `<placeholder>`, e
  nenhum id de nó que seja palavra reservada do Mermaid (`end`, `call`,
  `click`, `class`, `style`...). Um diagrama mostra só o que o código ou
  uma execução real mostram (o mesmo da seção 4); o que for hipotético é
  rotulado como "(hipotético)". Renderize antes do commit:
  `npx -p @mermaid-js/mermaid-cli mmdc -i diagrama.mmd -o diagrama.svg`.
- Comandos copiáveis, com a saída real em um bloco `text` logo abaixo;
  placeholders no formato `<seu-valor>`.

## 9. Fluxo de trabalho ao adicionar ou alterar um módulo

1. Leia um módulo existente inteiro (README, exemplos, teste).
2. Consulte as fontes oficiais de tudo o que vai ensinar (seção 4).
3. Escreva os exemplos seguindo o contrato (seção 3) e rode cada um.
4. Escreva os testes; `uv run pytest tests/unit/test_NN_tema.py -v`;
   quebre o exemplo de propósito e confira que um teste falha.
5. Escreva o README com as saídas reais; `make docs-fix`; renderize os
   diagramas.
6. `make all` (lint, typecheck, docs, doctest, coverage, run-all).
7. Atualize `docs/TRILHA.md`, `README.md`, `docs/GLOSSARIO.md`,
   `docs/SOLUCAO-DE-PROBLEMAS.md` e `CHANGELOG.md`.
8. Git: branch padrão `master`; **não faça commit nem push sem um pedido
   explícito**.

## 10. O que não fazer

- Não invente uma função, parâmetro, comportamento, mensagem de erro,
  saída, versão ou data.
- Não escreva uma saída "de cabeça" - rode o código.
- Não use pacotes de terceiros nos exemplos.
- Não deixe a cobertura cair abaixo de 80%, nem um sumário desatualizado ou
  um link quebrado (`make docs`).
- Não renumere módulos.
- Não substitua um comando documentado por extenso por um alvo do `make`.
- Não altere `learning_python/` nem a `LICENSE` sem um pedido.
- Não faça commit nem push sem um pedido.

## 11. Notas de ambiente

Testado no Ubuntu 22.04 (amd64) com Python 3.14.7, uv 0.12, mise 2026.9 e
GNU make 4.3, em outubro de 2026. Não há pipeline de CI configurado; rode
`make all` antes de cada pull request. A primeira execução de `make setup`
precisa de rede (PyPI e, se o Python 3.14 não estiver instalado, o
download do Python); depois disso, tudo roda offline.
