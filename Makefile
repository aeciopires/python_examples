# Makefile do python_examples.
#
# Cada alvo aqui é um *atalho* para comandos documentados passo a passo em
# REQUIREMENTS.md, CONTRIBUTING.md, docs/TESTES.md e no README de cada
# módulo. Aprenda a forma longa primeiro - `uv run python <arquivo>`,
# `uv run pytest` ... - e use os atalhos depois de saber o que eles rodam.
# `make` (ou `make help`) lista todos os alvos.
#
# Manual do GNU make: https://www.gnu.org/software/make/manual/make.html

SHELL := /bin/bash

.DEFAULT_GOAL := help

# O número do módulo (01 a 13), para run e test-module: make run MODULO=03
MODULO ?=
# Um arquivo, para run-file: make run-file ARQUIVO=modulos/03_controle_de_fluxo/exemplos/adivinhe.py
ARQUIVO ?=
# SKIP_COVERAGE_CHECK=1 faz `make coverage` só mostrar o relatório, sem falhar abaixo de 80%.
SKIP_COVERAGE_CHECK ?=

# A pasta do módulo escolhido (ex.: MODULO=03 -> modulos/03_controle_de_fluxo).
PASTA_MODULO = $(wildcard modulos/$(MODULO)_*)

.PHONY: help check setup run run-all run-file test test-module doctest lint format \
	typecheck coverage docs docs-fix all clean

help: ## Mostra esta lista de alvos
	@echo "Alvos:"
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-12s %s\n", $$1, $$2}'
	@echo ""
	@echo "Exemplos:"
	@echo "  make run MODULO=03          make test-module MODULO=03"
	@echo "  make run-file ARQUIVO=modulos/03_controle_de_fluxo/exemplos/adivinhe.py"

check: ## Verifica o sistema operacional e as ferramentas necessárias (REQUIREMENTS.md, seção 3)
	@bash scripts/check-deps.sh

setup: ## Instala Python e uv com o mise (se houver) e as dependências com o uv
	@if command -v mise >/dev/null 2>&1; then mise trust --quiet && mise install; \
	else echo "mise não encontrado: pulando 'mise install' (veja REQUIREMENTS.md, seção 3.3)."; fi
	uv sync

# --- executando os exemplos -----------------------------------------------------

# Os exemplos rodam sem teclado (< /dev/null); o jogo adivinhe.py detecta
# isso e encerra. Para jogar de verdade, use `make run-file`.
run: ## Executa todos os exemplos de UM módulo (MODULO=03)
	@if [ -z "$(MODULO)" ]; then \
		echo "Escolha o módulo: make run MODULO=03 (veja docs/TRILHA.md)." >&2; exit 1; \
	fi
	@if [ -z "$(PASTA_MODULO)" ]; then \
		echo "Módulo '$(MODULO)' não encontrado em modulos/ - use dois dígitos (01 a 13)." >&2; exit 1; \
	fi
	@set -e; for arquivo in $(PASTA_MODULO)/exemplos/*.py; do \
		echo ""; echo "===== $$arquivo ====="; \
		uv run python "$$arquivo" < /dev/null; \
	done

run-all: ## Executa todos os exemplos de todos os módulos, em ordem
	@set -e; for arquivo in modulos/*/exemplos/*.py; do \
		echo ""; echo "===== $$arquivo ====="; \
		uv run python "$$arquivo" < /dev/null; \
	done
	@echo ""; echo "Todos os exemplos rodaram sem erro."

run-file: ## Executa um único arquivo, com teclado (ARQUIVO=caminho/do/arquivo.py)
	@if [ -z "$(ARQUIVO)" ]; then \
		echo "Escolha o arquivo: make run-file ARQUIVO=modulos/01_primeiros_passos/exemplos/ola_mundo.py" >&2; exit 1; \
	fi
	uv run python "$(ARQUIVO)"

# --- testes e qualidade -----------------------------------------------------------

test: ## Executa todos os testes (pytest)
	uv run pytest -q

test-module: ## Executa os testes de UM módulo, um por linha (MODULO=03)
	@if [ -z "$(MODULO)" ]; then \
		echo "Escolha o módulo: make test-module MODULO=03" >&2; exit 1; \
	fi
	uv run pytest tests/unit/test_$(MODULO)_*.py -v

# Cada arquivo roda com a própria pasta no caminho de busca (PYTHONPATH),
# para que os exemplos que importam outros exemplos (módulo 06) funcionem.
doctest: ## Executa os exemplos ">>>" das docstrings (exemplos e scripts) com o doctest
	@set -e; for arquivo in modulos/*/exemplos/*.py; do \
		PYTHONPATH="$$(dirname "$$arquivo")" uv run python -m doctest "$$arquivo"; \
	done
	uv run python -m doctest scripts/verificar_docs.py
	@echo "doctest: nenhuma falha."

lint: ## Procura problemas de estilo e erros prováveis com o ruff
	uv run ruff check .
	uv run ruff format --check .

format: ## Formata o código com o ruff (altera os arquivos)
	uv run ruff format .
	uv run ruff check --fix .

# As pastas dos módulos começam com um número (01_primeiros_passos), que não
# é um nome de pacote Python válido, então cada pasta de exemplos é
# verificada separadamente.
typecheck: ## Verifica as anotações de tipo com o mypy
	uv run mypy tests scripts
	@set -e; for pasta in modulos/*/exemplos/; do \
		echo "mypy $$pasta"; \
		MYPYPATH="$$pasta" uv run mypy --explicit-package-bases --no-error-summary "$$pasta"; \
	done

coverage: ## Testes com relatório de cobertura (falha abaixo de 80%; SKIP_COVERAGE_CHECK=1 só mostra)
	@if [ -n "$(SKIP_COVERAGE_CHECK)" ]; then \
		echo "SKIP_COVERAGE_CHECK definido: mostrando a cobertura sem exigir o mínimo de 80%."; \
	fi
	uv run pytest tests --cov --cov-report=term-missing --cov-report=html \
		$(if $(SKIP_COVERAGE_CHECK),--cov-fail-under=0)

docs: ## Verifica os sumários (TOC) e os links relativos de todos os .md (CLAUDE.md, seção 8)
	uv run python scripts/verificar_docs.py

docs-fix: ## Regenera os sumários (TOC) de todos os .md
	uv run python scripts/verificar_docs.py --corrigir

all: lint typecheck docs doctest coverage run-all ## Tudo: lint, tipos, docs, doctest, testes com cobertura e todos os exemplos

clean: ## Apaga caches e relatórios gerados (não apaga o .venv)
	find . -path ./.venv -prune -o -type d -name __pycache__ -print -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
