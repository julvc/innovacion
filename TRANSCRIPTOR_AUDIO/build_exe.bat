@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Build -- Transcriptor de Video Pro

echo.
echo ================================================================
echo  Transcriptor de Video Pro v1.0  --  Build EXE
echo  SONDA  /  Julio Varas Contreras  /  Mayo 2026
echo ================================================================
echo.
echo  ADVERTENCIA: El ejecutable incluye torch y whisper.
echo  Tamano estimado: 1.5 - 2.5 GB. Build: 5-15 minutos.
echo  Los modelos Whisper NO se incluyen (se descargan al primer uso).
echo.

REM ── 1. Verificar Python ──────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH.
    pause & exit /b 1
)
echo [OK] Python detectado.

REM ── 2. Instalar / actualizar PyInstaller ─────────────────────────
echo.
echo [INFO] Verificando PyInstaller...
python -m pip install --quiet --upgrade pyinstaller
echo [OK] PyInstaller listo.

REM ── 3. Generar icon.ico si hay PNG disponibles ───────────────────
echo.
echo [INFO] Generando icon.ico...
python -c ^
"from PIL import Image; from pathlib import Path; ^
logo = Path('DF 500X500 BLANCO 1.png'); ^
(Image.open(logo).convert('RGBA').save('icon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]), print('icon.ico generado desde DF logo')) if logo.is_file() else print('Logo DF no encontrado')" 2>nul
echo.

REM ── 4. Limpiar builds anteriores ─────────────────────────────────
echo [INFO] Limpiando builds anteriores...
if exist "Transcriptor.exe"          del /f /q "Transcriptor.exe"
if exist "dist"                      rd /s /q "dist"
if exist "build\Transcriptor"        rd /s /q  "build\Transcriptor"
if exist "Transcriptor.spec"         del /f /q "Transcriptor.spec"
echo [OK] Limpieza completada.

REM ── 5. Compilar ──────────────────────────────────────────────────
echo.
echo [INFO] Compilando (esto tarda varios minutos)...
echo.

set ICON_ARG=
if exist "icon.ico" set ICON_ARG=--icon="icon.ico"

set DF_ARG=
if exist "DF 500X500 BLANCO 1.png" set DF_ARG=--add-data="DF 500X500 BLANCO 1.png;."

python -m PyInstaller ^
    --clean --noconfirm --onefile --console ^
    --name="Transcriptor" ^
    --distpath="." ^
    %ICON_ARG% ^
    %DF_ARG% ^
    --exclude-module="whisper" ^
    --exclude-module="torch" ^
    --exclude-module="torchvision" ^
    --exclude-module="torchaudio" ^
    --exclude-module="numpy" ^
    --exclude-module="tqdm" ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] La compilacion fallo.
    pause & exit /b 1
)

REM ── 6. Verificar salida ───────────────────────────────────────────
if not exist "Transcriptor.exe" (
    echo [ERROR] El EXE no fue generado.
    pause & exit /b 1
)

echo.
echo ================================================================
echo  BUILD EXITOSO  --  SONDA
echo ================================================================
echo.
for %%F in ("Transcriptor.exe") do (
    echo  Archivo  : Transcriptor.exe
    set /a SIZE_MB=%%~zF / 1048576
    echo  Tamano   : %%~zF bytes  (~!SIZE_MB! MB)
)
echo.
echo  Distribuir:
echo    Transcriptor.exe   (copia unica, sin instalacion)
echo.
echo  NOTA: El ejecutable ahora NO incluye librerias pesadas (Torch/Whisper).
echo        El usuario final debe ejecutar 'setup_dependencias.bat' para
echo        descargarlas en un entorno local antes de usar la aplicacion.
echo.

set /p ABRIR="Abrir carpeta de destino? (S/N): "
if /i "!ABRIR!"=="S" explorer .

echo.
pause
