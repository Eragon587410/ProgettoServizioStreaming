@echo off
REM -----------------------------
REM start.bat - avvia container Flask e apre shell interattiva
REM -----------------------------

set FLASK_IMAGE=flask-image
set FLASK_CONTAINER=flask

REM --- Controlla se il container Flask esiste ---
docker ps -a --format "{{.Names}}" | findstr /i "%FLASK_CONTAINER%" >nul
if %errorlevel%==0 (
    echo Container %FLASK_CONTAINER% già esistente, avvio in shell mode...
    docker start -ai %FLASK_CONTAINER%
) else (
    echo Creazione e avvio container Flask in shell mode...
    docker run --rm --name %FLASK_CONTAINER% -it -p 5000:5000 -v "%cd%\webServer\flaskr:/app" -w /app %FLASK_IMAGE% bash 
)

echo Sei dentro il container Flask.
pause
