@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Instalador -- Transcriptor de Video Pro

echo.
echo ================================================================
echo  Transcriptor de Video Pro v1.0  --  Instalacion Portable
echo  SONDA  /  Julio Varas Contreras  /  Mayo 2026
echo ================================================================
echo.
echo  Este script configurara un entorno aislado y descargara
echo  las dependencias necesarias (~2 GB) en esta misma carpeta.
echo.

REM -- 1. Verificar Python ------------------------------------------
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH.
    echo         Descarga desde: https://www.python.org/downloads/
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo [OK] Detectado %%v

REM -- 2. Descargar e instalar ffmpeg localmente --------------------
echo.
if not exist "bin\ffmpeg.exe" (
    echo [INFO] Descargando ffmpeg portable ^(esto puede tardar unos segundos^)...
    mkdir bin 2>nul
    curl -L -o ffmpeg.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    echo [INFO] Extrayendo ffmpeg...
    tar -xf ffmpeg.zip
    move /y "ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "bin\" >nul
    move /y "ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe" "bin\" >nul
    rmdir /s /q "ffmpeg-master-latest-win64-gpl"
    del /q "ffmpeg.zip"
    echo [OK] ffmpeg instalado en carpeta local bin/
) else (
    echo [OK] ffmpeg portable ya esta instalado.
)

REM -- 3. Verificar o crear entorno virtual (venv) ------------------
echo.
if exist "env\Scripts\python.exe" (
    env\Scripts\python.exe -c "import whisper" >nul 2>&1
    if not errorlevel 1 (
        echo [OK] El entorno virtual y la IA ya estan instalados correctamente.
        goto :fin_instalacion
    )
    echo [INFO] Instalacion previa incompleta o corrupta. Limpiando...
    rmdir /s /q "env"
)
echo [INFO] Configurando Entorno Virtual Aislado (venv)...
python -m venv env
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause & exit /b 1
)
call env\Scripts\activate.bat

echo.
echo [INFO] Instalando Torch (CPU)... ^(Descarga de ~1.5 GB^)
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo [INFO] Instalando dependencias de IA (Whisper)...
python -m pip install -U openai-whisper

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de paquetes.
    pause & exit /b 1
)

:fin_instalacion
echo.
echo [INFO] Verificando instalacion...
env\Scripts\python.exe -c "import whisper; print('[OK] whisper importado correctamente')"

echo.
echo ================================================================
echo  SETUP COMPLETADO  --  SONDA
echo ================================================================
echo.
echo  [PASO COMPLETADO CON EXITO]
echo  Ya puedes usar la aplicacion.
echo.

set /p ABRIR="Iniciar la aplicacion ahora? (S/N): "
if /i "!ABRIR!"=="S" (
    if exist "Transcriptor.exe" (
        start "" "Transcriptor.exe"
    ) else if exist "main.py" (
        start "" "env\Scripts\pythonw.exe" main.py
    ) else (
        echo [AVISO] Aplicacion no encontrada. Compila el ejecutable primero.
    )
)

echo.
pause
