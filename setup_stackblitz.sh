#!/bin/bash

echo "------------------------------------------------"
echo "  PySwissShef Laboratory: Static Tasting Room   "
echo "------------------------------------------------"

# 1. Environment Check
if command -v pip > /dev/null 2>&1
then
    echo "[+] pip found. Initializing full Laboratory dependencies..."
    pip install -r requirements.txt
    echo "[+] Dependencies loaded. Run 'npm run portal' to start the interactive Lab."
else
    echo "[!] pip not found (StackBlitz WASM Limit)."
    echo "------------------------------------------------"
    echo "NOTICE: One-Click Tasting Room Initialized"
    echo "------------------------------------------------"
    echo "This environment is currently optimized for UI Browsing."
    echo "The gourmet layout should appear in your preview window automatically."
    echo ""
    echo "To EAT (Execute) automation recipes with high-heat support:"
    echo ">>> USE REPLIT OR CODESPACES <<<"
    print " (See docs/LAB_STATIONS.md for links) "
    echo "------------------------------------------------"
fi

echo "[+] Serving Static Tasting Room..."
npx http-server ./ -p 8000
