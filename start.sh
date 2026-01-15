#!/bin/bash
# -----------------------------
# start.sh - avvia container Flask e apre shell interattiva
# -----------------------------

FLASK_IMAGE="flask-image"
FLASK_CONTAINER="flask"


if docker ps -a --format "{{.Names}}" | grep -iq "$FLASK_CONTAINER"; then
    echo "Container $FLASK_CONTAINER già esistente, avvio in shell mode..."
    docker start -ai "$FLASK_CONTAINER"
else
    echo "Creazione e avvio container Flask in shell mode..."
    docker run --rm --name "$FLASK_CONTAINER" --network streaming-net -it -p 5000:5000 \
        -v "$(pwd)/webServer/flaskr:/app" -w /app "$FLASK_IMAGE" bash
fi

echo "Sei dentro il container Flask."
read -p "Premi invio per continuare..."
