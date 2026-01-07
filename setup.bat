@echo off
REM -----------------------------
REM setup.bat - crea immagini e container base
REM -----------------------------

REM --- Configurazioni ---
set FLASK_IMAGE=flask-image
set FLASK_CONTAINER=flask
set MYSQL_CONTAINER=testDB
set HLS_CONTAINER=hls-server

REM --- Crea DB MySQL se non esiste ---
docker ps -a --format "{{.Names}}" | findstr /i "%MYSQL_CONTAINER%" >nul
if %errorlevel%==0 (
    echo Container %MYSQL_CONTAINER% già esistente, skipping...
) else (
    echo Creazione container MySQL...
    docker run -d --name %MYSQL_CONTAINER% -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=streaming -p 3306:3306 mysql:8
)

REM --- Crea HLS server se non esiste ---
docker ps -a --format "{{.Names}}" | findstr /i "%HLS_CONTAINER%" >nul
if %errorlevel%==0 (
    echo Container %HLS_CONTAINER% già esistente, skipping...
) else (
    echo Creazione container HLS...
    docker run -d --name %HLS_CONTAINER% -p 8080:80 -v "%cd%\streamingServer\film\hls:/usr/share/nginx/html/hls:ro" nginx:latest
)

REM --- Build dell'immagine Flask ---
echo Costruzione immagine Flask...
docker build -t %FLASK_IMAGE% -f "%cd%\webServer\Dockerfile" "%cd%\webServer\flaskr"

echo Setup completato!
pause
