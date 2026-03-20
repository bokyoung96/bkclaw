#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-${OLLAMA_VERSION:-0.7.0}}"
ARCH_RAW="$(uname -m)"
case "$ARCH_RAW" in
  x86_64) ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
  *) echo "[ERROR] Unsupported architecture: $ARCH_RAW" >&2; exit 1 ;;
esac

INSTALL_ROOT="${OLLAMA_INSTALL_ROOT:-$HOME/.local/lib/ollama}"
BIN_DIR="${OLLAMA_BIN_DIR:-$HOME/.local/bin}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$INSTALL_ROOT" "$BIN_DIR"
cd "$TMP_DIR"

echo "[install] version=$VERSION arch=$ARCH"
curl -fL "https://ollama.com/download/ollama-linux-${ARCH}.tgz?version=${VERSION}" -o ollama.tgz
tar -xzf ollama.tgz -C "$INSTALL_ROOT"
ln -sf "$INSTALL_ROOT/ollama" "$BIN_DIR/ollama"

echo "[ok] installed to $INSTALL_ROOT"
echo "[ok] binary link: $BIN_DIR/ollama"
echo "[next] run: ~/.openclaw/workspace/scripts/start_local_ollama.sh"
