#!/usr/bin/env bash
# Verifica se o seu sistema operacional é suportado e se as ferramentas que
# este repositório usa estão instaladas - veja REQUIREMENTS.md, especialmente
# a seção 1 (sistemas operacionais suportados) e a seção 3 (software
# necessário), com as quais as verificações e versões deste script são
# mantidas em sincronia.
#
# Rode com `make check` (veja o Makefile) ou diretamente:
#   bash scripts/check-deps.sh
#
# Escrito para o bash 3.2 (o /bin/bash padrão do macOS) e também para bash
# mais novos - sem arrays associativos, sem `${var,,}`, sem `sort -V` (uma
# opção só do GNU que o `sort` BSD do macOS não tem) - veja ver_ge() abaixo.
# Nunca instala nada.

set -u

FAIL_COUNT=0
WARN_COUNT=0

# --- funções de saída ---------------------------------------------------------

if [ -t 1 ]; then
  C_OK="\033[32m"
  C_WARN="\033[33m"
  C_FAIL="\033[31m"
  C_RESET="\033[0m"
else
  C_OK=""
  C_WARN=""
  C_FAIL=""
  C_RESET=""
fi

section() {
  echo ""
  echo "== $1 =="
}

ok() {
  printf "  ${C_OK}[ OK ]${C_RESET} %s\n" "$1"
}

warn() {
  printf "  ${C_WARN}[AVISO]${C_RESET} %s\n" "$1"
  WARN_COUNT=$((WARN_COUNT + 1))
}

fail() {
  printf "  ${C_FAIL}[FALHA]${C_RESET} %s\n" "$1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

# ver_ge TEM QUER - verdadeiro (código 0) se a versão TEM >= QUER, comparando
# campos numéricos separados por ponto (então "3.9" < "3.10", diferente de
# uma comparação de texto). Feito em awk puro porque o `sort` BSD do macOS
# não tem `-V` - veja o cabeçalho do arquivo.
ver_ge() {
  awk -v have="$1" -v want="$2" '
    BEGIN {
      n1 = split(have, h, ".")
      n2 = split(want, w, ".")
      max = (n1 > n2 ? n1 : n2)
      for (i = 1; i <= max; i++) {
        hv = (i <= n1) ? h[i] + 0 : 0
        wv = (i <= n2) ? w[i] + 0 : 0
        if (hv > wv) { exit 0 }
        if (hv < wv) { exit 1 }
      }
      exit 0
    }'
}

# first_version TEXTO - extrai o primeiro "N.N" ou "N.N.N" encontrado no TEXTO
# (a saída de --version de cada ferramenta verificada aqui começa pela
# versão da própria ferramenta).
first_version() {
  echo "$1" | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -n 1
}

REQUIREMENTS_HINT="Veja REQUIREMENTS.md, seção 3 (Software necessário), para o que é e o comando de instalação para o seu sistema."

# --- sistema operacional -------------------------------------------------------

check_os() {
  section "Sistema operacional (REQUIREMENTS.md, seção 1)"

  os="$(uname -s)"
  arch="$(uname -m)"

  case "$os" in
    Linux)
      distro="desconhecida"
      distro_ver="desconhecida"
      if [ -r /etc/os-release ]; then
        # shellcheck disable=SC1091  # arquivo padrão do sistema, não deste repositório
        distro="$(. /etc/os-release && echo "$ID")"
        # shellcheck disable=SC1091
        distro_ver="$(. /etc/os-release && echo "$VERSION_ID")"
      fi
      if [ "$distro" != "ubuntu" ]; then
        warn "Distribuição Linux '$distro' ($arch) detectada - este repositório é testado no Ubuntu 22.04/24.04/26.04 (amd64). Outras distribuições devem funcionar; veja REQUIREMENTS.md, seção 1."
      elif [ "$arch" != "x86_64" ]; then
        warn "Ubuntu $distro_ver em '$arch' detectado - este repositório é testado em amd64 (x86_64); veja REQUIREMENTS.md, seção 1."
      else
        case "$distro_ver" in
          22.04 | 24.04 | 26.04)
            ok "Ubuntu $distro_ver ($arch) - suportado"
            ;;
          *)
            warn "Ubuntu $distro_ver ($arch) detectado - este repositório é testado no 22.04/24.04/26.04; o $distro_ver provavelmente funciona, mas veja REQUIREMENTS.md, seção 1."
            ;;
        esac
      fi
      ;;
    Darwin)
      macos_ver="$(sw_vers -productVersion 2>/dev/null || echo "")"
      if [ "$arch" != "arm64" ] && [ "$arch" != "x86_64" ]; then
        warn "macOS em arquitetura inesperada '$arch' - veja REQUIREMENTS.md, seção 1."
      elif [ -z "$macos_ver" ]; then
        warn "macOS ($arch) detectado, mas não foi possível descobrir a versão."
      elif ver_ge "$macos_ver" "13.0"; then
        ok "macOS $macos_ver ($arch) - suportado"
      else
        warn "macOS $macos_ver ($arch) detectado - este repositório é feito para macOS 13+; veja REQUIREMENTS.md, seção 1."
      fi
      ;;
    *)
      fail "O sistema '$os' não é suportado diretamente. No Windows, instale o WSL2 com Ubuntu e rode esta verificação dentro dele - veja REQUIREMENTS.md, seção 1."
      ;;
  esac
}

# --- software necessário ---------------------------------------------------------

check_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    warn "python3 não encontrado no PATH - tudo bem: 'mise install' ou 'uv sync' instalam o Python 3.14 (veja REQUIREMENTS.md, seções 3.3 e 4)."
    return
  fi
  have="$(first_version "$(python3 --version 2>&1)")"
  if [ -z "$have" ]; then
    warn "python3 encontrado, mas não foi possível ler a versão."
  elif ver_ge "$have" "3.14"; then
    ok "Python $have (3.14 fixado em .python-version/mise.toml)"
  else
    warn "Python $have encontrado, mas este repositório fixa o 3.14 - rode 'mise install', ou deixe o 'uv sync' baixar o 3.14 (veja REQUIREMENTS.md, seções 3.3 e 4)."
  fi
}

check_uv() {
  if ! command -v uv >/dev/null 2>&1; then
    fail "uv não encontrado. $REQUIREMENTS_HINT"
    return
  fi
  have="$(first_version "$(uv --version 2>&1)")"
  ok "uv${have:+ $have} encontrado"
}

check_mise() {
  if ! command -v mise >/dev/null 2>&1; then
    warn "mise não encontrado (recomendado, não obrigatório - instala o Python e o uv fixados no mise.toml). Veja REQUIREMENTS.md, seção 3.3."
    return
  fi
  have="$(first_version "$(mise --version 2>&1)")"
  ok "mise${have:+ $have} encontrado"
}

# Uma verificação simples de "está no PATH?": obrigatório falha, opcional avisa.
check_command() {
  name="$1"; level="$2"; why="$3"
  if command -v "$name" >/dev/null 2>&1; then
    have="$(first_version "$("$name" --version 2>&1 | head -n 1)")"
    ok "$name${have:+ $have} encontrado"
  elif [ "$level" = "obrigatorio" ]; then
    fail "$name não encontrado ($why). $REQUIREMENTS_HINT"
  else
    warn "$name não encontrado (opcional - $why; veja REQUIREMENTS.md, seção 3)."
  fi
}

# --- principal ------------------------------------------------------------------

check_os

section "Software necessário (REQUIREMENTS.md, seção 3)"
check_uv
check_python
check_command git obrigatorio "baixa este repositório"
check_command make obrigatorio "roda os atalhos do Makefile"
check_command curl obrigatorio "baixa os instaladores do uv e do mise"

section "Software recomendado"
check_mise

section "Software opcional"
check_command npx opcional "renderiza os diagramas Mermaid ao contribuir - CONTRIBUTING.md"

echo ""
echo "======================================================================"
if [ "$FAIL_COUNT" -gt 0 ]; then
  printf "${C_FAIL}%s item(ns) obrigatório(s) ausente(s) ou não suportado(s), %s aviso(s).${C_RESET}\n" "$FAIL_COUNT" "$WARN_COUNT"
  echo ""
  echo "Veja em REQUIREMENTS.md para que serve cada item [FALHA] e o"
  echo "comando de instalação para o seu sistema:"
  echo "  - Ubuntu (e WSL2): REQUIREMENTS.md, seção 3.1"
  echo "  - macOS:           REQUIREMENTS.md, seção 3.2"
  echo "======================================================================"
  exit 1
else
  printf "${C_OK}Todo o software obrigatório foi encontrado e o seu sistema é suportado${C_RESET} (%s aviso(s) - veja REQUIREMENTS.md para os itens marcados com [AVISO]).\n" "$WARN_COUNT"
  echo "======================================================================"
  exit 0
fi
