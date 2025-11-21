#!/usr/bin/env bash
set -e
# Executa watcher.py a partir da pasta project-root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."
cd project-root
python3 watcher.py
