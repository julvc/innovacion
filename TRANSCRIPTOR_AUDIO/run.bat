@echo off
cd /d "%~dp0"
echo ================================================================
echo  Transcriptor de Video Pro v1.0  --  SONDA
echo ================================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH.
    pause & exit /b 1
)

python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion termino con error.
    pause
)
