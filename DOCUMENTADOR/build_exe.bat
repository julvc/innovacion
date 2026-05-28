@echo off
chcp 65001 > nul
cls

echo ====================================================
echo   DOCUMENTADOR DE PROYECTOS - Build PyInstaller
echo ====================================================
echo.

REM ── Verificar entorno virtual ────────────────────────────────
if not exist "env\Scripts\activate.bat" (
    echo [ERROR] No se encontro el entorno virtual 'env'.
    echo Ejecuta primero: setup_dependencias.bat
    pause
    exit /b 1
)

call env\Scripts\activate.bat
echo [OK] Entorno virtual activado.

REM ── PyInstaller disponible? ──────────────────────────────────
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo instalar PyInstaller.
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller disponible.

REM ── Dependencias del proyecto ────────────────────────────────
echo Verificando dependencias...
pip install -r requirements.txt --quiet
echo [OK] Dependencias verificadas.

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

REM ── Compilar ─────────────────────────────────────────────────
echo.
echo Compilando con PyInstaller (puede tardar 1-3 minutos)...
echo.
pyinstaller documentador.spec --noconfirm

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
