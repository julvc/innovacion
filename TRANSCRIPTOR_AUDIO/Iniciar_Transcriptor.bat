@echo off
cd /d "%~dp0"
title Transcriptor de Video Pro

if not exist "env\Scripts\pythonw.exe" (
    echo =========================================================
    echo [ERROR] El entorno de la aplicacion no esta instalado.
    echo Por favor, ejecuta 'setup_dependencias.bat' por primera 
    echo vez para descargar e instalar los componentes necesarios.
    echo =========================================================
    pause
    exit /b 1
)

start "" "env\Scripts\python.exe" main.py