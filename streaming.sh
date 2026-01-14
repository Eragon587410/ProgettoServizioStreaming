#!/bin/bash
# -----------------------------
# streaming.sh - comandi locali
# -----------------------------

if [ "$1" = "setup" ]; then
    ./setup.sh
    exit 0
fi

if [ "$1" = "run" ]; then
    ./start.sh
    exit 0
fi

echo "Comandi disponibili:"
echo "  ./streaming.sh setup   - esegue setup.sh"
echo "  ./streaming.sh run     - esegue start.sh"
