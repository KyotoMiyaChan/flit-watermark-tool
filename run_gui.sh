#!/bin/bash
PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJ_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install Pillow PyQt5
else
    source "$VENV_DIR/bin/activate"
fi
python "$PROJ_DIR/main.py"
