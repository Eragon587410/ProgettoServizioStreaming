#!/bin/bash
# -----------------------------
# setup.sh - crea immagini e container base
# -----------------------------


FLASK_IMAGE="flask-image"
FLASK_CONTAINER="flask"
MYSQL_CONTAINER="testDB"
HLS_CONTAINER="hls-server"

docker network create streaming-net 2>/dev/null || true

if docker ps -a --format "{{.Names}}" | grep -iq "$MYSQL_CONTAINER"; then
    echo "Container $MYSQL_CONTAINER già esistente, skipping..."
else
    echo "Creazione container MySQL..."
    docker run -d --name "$MYSQL_CONTAINER" \
        --network streaming-net \
        -e MYSQL_ROOT_PASSWORD=root \
        -e MYSQL_DATABASE=streaming \
        -p 3306:3306 mysql:8
fi


if docker ps -a --format "{{.Names}}" | grep -iq "$HLS_CONTAINER"; then
    echo "Container $HLS_CONTAINER già esistente, skipping..."
else
    echo "Creazione container HLS..."
    docker run -d --name "$HLS_CONTAINER" \
        --network streaming-net \
        -p 8080:80 \
        -v "$(pwd)/streamingServer/film/hls:/usr/share/nginx/html/hls:ro" \
        nginx:latest
fi


echo "Costruzione immagine Flask..."
docker build -t "$FLASK_IMAGE" -f "$(pwd)/webServer/Dockerfile" "$(pwd)/webServer/flaskr"

echo "Setup completato!"
read -p "Premi invio per continuare..."
