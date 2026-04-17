#!/bin/bash

echo "------------------------------------------------"
echo "  PySwissShef Laboratory: StackBlitz Bootstrap  "
echo "------------------------------------------------"

# 1. Environment Check
if command -v pip > /dev/null 2>&1
then
    echo "[+] pip found. Initializing dependencies..."
    pip install -r requirements.txt
else
    echo "[!] pip not found (Common in StackBlitz WASM containers)."
    echo "------------------------------------------------"
    echo "NOTICE: StackBlitz Preview Mode Only"
    echo "------------------------------------------------"
    echo "This environment is currently restricted to 'In-Process' browsing."
    echo "You can still browse the Lab UI and check Recipe documentation."
    echo ""
    echo "For full automation execution with high-heat dependencies:"
    echo ">>> USE REPLIT OR CODESPACES <<<"
    echo "------------------------------------------------"
fi

echo "[+] Starting Lab Portal..."
python main.py --web
