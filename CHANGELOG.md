<!-- TOC -->

- [Changelog](#changelog)
  - [\[Não lançado\]](#não-lançado)
    - [Adicionado](#adicionado)
    - [Alterado](#alterado)
  - [\[0.2.0\] - 2026-10-03](#020---2026-10-03)
    - [Adicionado](#adicionado-1)
    - [Alterado](#alterado-1)
    - [Mantido](#mantido)
  - [\[0.1.0\] - 2018-08-28](#010---2018-08-28)
    - [Adicionado](#adicionado-2)

<!-- TOC -->

# Changelog

Todas as mudanças relevantes deste projeto são registradas neste arquivo.
O formato segue, de forma livre, o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Não lançado]

### Adicionado

- Módulo 13, `modulos/13_python_para_infraestrutura/` (nova fase 5,
  "Python no trabalho"): Python para quem atua com infraestrutura (DevOps
  engineer, SRE, cloud architect), só com a biblioteca padrão e sem rede.
  Seis exemplos - `comandos.py` (`subprocess.run`, `shlex`,
  `shutil.which`), `configuracao.py` (valores padrão, `tomllib` e
  variáveis de ambiente), `analisar_logs.py` (`argparse`, `logging`, `re`,
  `Counter` e código de saída), `redes.py` (`ipaddress`: CIDR, sub-redes,
  sobreposição), `retentativas.py` (backoff exponencial) e
  `integridade.py` (SHA-256 com `hashlib.file_digest`) - e o README com
  analogias, diagramas, saídas reais, erros comuns e exercícios.
- `tests/unit/test_13_python_para_infraestrutura.py`.
- Termos novos no `docs/GLOSSARIO.md` e mensagens novas no
  `docs/SOLUCAO-DE-PROBLEMAS.md`.

### Alterado

- `README.md`, `docs/TRILHA.md`, `CLAUDE.md` e `Makefile` passam a contar
  13 módulos.

## [0.2.0] - 2026-10-03

Reescrita do repositório como uma trilha de Python para iniciantes, em
pt-BR, seguindo as convenções do repositório `learning-ecs`, do mesmo
autor (guardrails, mise, uv, Makefile, testes e documentação).

### Adicionado

- 12 módulos em `modulos/`, cada um com README (visão geral, analogias,
  diagramas Mermaid, saídas reais, erros comuns com as mensagens reais do
  Python 3.14, exercícios e referências oficiais) e exemplos executáveis
  (34 arquivos, mais o pacote `geometria` do módulo 06; só biblioteca
  padrão): 01 primeiros passos, 02 variáveis e tipos, 03 controle de
  fluxo, 04 funções, 05 estruturas de dados,
  06 módulos e pacotes, 07 erros e exceções, 08 arquivos, 09 classes e
  objetos, 10 testes, 11 anotações de tipo, 12 ambientes virtuais e
  dependências.
- Testes com pytest em `tests/`: um arquivo por módulo (compara a saída de
  cada exemplo com a do README e testa limites e erros), um teste que
  executa todos os exemplos sem teclado, os exemplos de unittest e doctest
  do módulo 10, e os testes de `scripts/verificar_docs.py`. Cobertura de
  ramos com mínimo de 80% (`make coverage`).
- Ferramentas: `pyproject.toml` e `uv.lock` (uv; pytest, pytest-cov, ruff
  e mypy no grupo `dev`), `.python-version` e `mise.toml` (Python 3.14 e
  uv), `Makefile` com `check`, `setup`, `run`, `run-all`, `run-file`,
  `test`, `test-module`, `doctest`, `lint`, `format`, `typecheck`,
  `coverage`, `docs`, `docs-fix`, `all` e `clean`.
- `scripts/check-deps.sh` (`make check`): verifica o sistema operacional
  (Ubuntu 22.04/24.04/26.04 amd64, macOS 13+ arm64/amd64; Windows via
  WSL2) e as ferramentas.
- `scripts/verificar_docs.py` (`make docs`, `make docs-fix`): gera e
  verifica os sumários e os links relativos de todos os `.md`.
- Documentação: `README.md` (reescrito em pt-BR), `REQUIREMENTS.md`,
  `CONTRIBUTING.md`, `CLAUDE.md`, `CHANGELOG.md`, `docs/TRILHA.md`,
  `docs/ARQUITETURA.md`, `docs/TESTES.md`, `docs/SOLUCAO-DE-PROBLEMAS.md` e
  `docs/GLOSSARIO.md`. Todos os diagramas Mermaid renderizados com o
  mermaid-cli antes do commit.
- `.gitignore` para caches do Python, cobertura e o `.venv`.

### Alterado

- Versões revisadas e traduzidas de `learning_python/guess.py` (módulo 03,
  `adivinhe.py`) e `learning_python/fish.py` (módulo 09, `heranca.py`).

### Mantido

- `learning_python/`: os exemplos originais (en-US), sem alterações, fora
  da trilha, do lint e dos testes.

## [0.1.0] - 2018-08-28

### Adicionado

- Exemplos de programas em Python 3 em `learning_python/` (en-US).
