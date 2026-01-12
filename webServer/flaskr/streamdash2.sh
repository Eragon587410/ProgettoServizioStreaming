#!/bin/bash
if [ "$1" = "run" ]; then
    bash /app/start.sh
    exit 0
fi
if [ "$1" = "setup" ]; then
    python -m db.setup
    exit 0
fi
if [ "$1" = "shell" ]; then
    python -m db.shell
    exit 0
fi



echo "Comandi disponibili:"
echo "streamdash run"
echo "streamdash setup"
echo "streamdash shell"
