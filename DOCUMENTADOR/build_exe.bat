@echo off
chcp 65001 > nul
cls

echo ====================================================
echo   DOCUMENTADOR DE PROYECTOS - Build PyInstaller
echo ====================================================
echo.

REM ── Verificar entorno virtual ────────────────────────────────
if not exist "env\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual 'env'.
    echo Ejecuta primero: setup_dependencias.bat
    pause
    exit /b 1
)

set "VENV_PYTHON=env\Scripts\python.exe"
set "VENV_PIP=env\Scripts\pip.exe"
set "VENV_PYINSTALLER=env\Scripts\pyinstaller.exe"
echo [OK] Entorno virtual detectado.

REM ── PyInstaller disponible? ──────────────────────────────────
%VENV_PYTHON% -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    %VENV_PIP% install pyinstaller
)

%VENV_PYTHON% -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo instalar PyInstaller.
    pause
    exit /b 1
)
echo [OK] PyInstaller disponible.

REM ── Dependencias del proyecto ────────────────────────────────
echo Verificando dependencias...
%VENV_PIP% install -r requirements.txt --quiet
echo [OK] Dependencias verificadas.

REM ── Cerrar proceso anterior si está corriendo ────────────────
echo Cerrando instancias anteriores del ejecutable...
taskkill /f /im "DocumentadorProyectos.exe" >nul 2>&1
timeout /t 2 /nobreak >nul

REM ── Limpiar builds anteriores ────────────────────────────────
echo Limpiando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist"  rmdir /s /q dist
echo [OK] Limpieza completada.

REM ── Crear carpetas necesarias ────────────────────────────────
if not exist "assets"    mkdir assets
if not exist "templates\web"    mkdir templates\web
if not exist "templates\mobile" mkdir templates\mobile
if not exist "templates\qa"     mkdir templates\qa

REM ── Regenerar icon.ico desde PNG (multi-tamaño) ──────────────
echo Generando icon.ico desde DF 500X500 AZUL 1.png...
%VENV_PYTHON% -c "from PIL import Image; img=Image.open('assets/DF 500X500 AZUL 1.png').convert('RGBA'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])" 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] Pillow no disponible, usando icon.ico existente.
) else (
    echo [OK] icon.ico generado con multiples tamanos.
)

REM ── Compilar ─────────────────────────────────────────────────
echo.
echo Compilando con PyInstaller (puede tardar 1-3 minutos)...
echo.

REM Asegurar que PyInstaller encuentre Tcl/Tk desde el entorno virtual
FOR /F "tokens=*" %%i IN ('%VENV_PYTHON% -c "import sys; print(sys.base_prefix)"') DO set "BASE_PYTHON=%%i"
set "TCL_LIBRARY=%BASE_PYTHON%\tcl\tcl8.6"
set "TK_LIBRARY=%BASE_PYTHON%\tcl\tk8.6"

%VENV_PYINSTALLER% main.py --noconfirm --name "DocumentadorProyectos" --windowed --icon "assets\icon.ico" --hidden-import tkinter --hidden-import tkinter.ttk --add-data "assets;assets"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller fallo. Revisa los mensajes anteriores.
    pause
    exit /b 1
)

REM ── Post-build: crear carpetas de datos ──────────────────────
echo.
echo Creando carpetas de datos en dist...
if not exist "dist\DocumentadorProyectos\projects" mkdir "dist\DocumentadorProyectos\projects"
if not exist "dist\DocumentadorProyectos\exports"  mkdir "dist\DocumentadorProyectos\exports"

echo.
echo ====================================================
echo   Build completado exitosamente!
echo.
echo   Ejecutable: dist\DocumentadorProyectos\DocumentadorProyectos.exe
echo   Distribuir: carpeta dist\DocumentadorProyectos\ completa
echo ====================================================
echo.
pause
