@echo off
REM -----------------------------
REM streaming.bat - comandi locali
REM -----------------------------

if "%1"=="setup" (
    call setup.bat
    goto :eof
)

if "%1"=="run" (
    call start.bat
    goto :eof
)

echo Comandi disponibili:
echo streaming setup   - esegue setup.bat
echo streaming run     - esegue start.bat
