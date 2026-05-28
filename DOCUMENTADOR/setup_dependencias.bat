@echo off
chcp 65001 > nul
cls

echo ====================================================
echo   DOCUMENTADOR DE PROYECTOS - Setup Dependencias
echo ====================================================
echo.

REM ── Verificar Python ─────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado.
    echo Descarga Python 3.10+ desde https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" al instalar.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do set PY_VER=%%v
echo [OK] %PY_VER% detectado.

REM ── Crear entorno virtual ────────────────────────────────────
if exist "env\Scripts\activate.bat" (
    echo [OK] Entorno virtual 'env' ya existe.
) else (
    echo Creando entorno virtual 'env'...
    python -m venv env
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado.
)

REM ── Activar entorno ──────────────────────────────────────────
call env\Scripts\activate.bat
echo [OK] Entorno virtual activado.

REM ── Actualizar pip ───────────────────────────────────────────
echo Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado.

REM ── Instalar dependencias ─────────────────────────────────────
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de dependencias.
    echo Revisa tu conexion a internet e intenta nuevamente.
    pause
    exit /b 1
)

REM ── Verificar instalacion ─────────────────────────────────────
echo.
echo Verificando dependencias instaladas...
python -c "import jinja2, docx, markdown, fpdf, keyring, requests, PIL; print('[OK] Todas las dependencias verificadas.')"
if %errorlevel% neq 0 (
    echo [WARN] Alguna dependencia no se instalo correctamente.
    echo Ejecuta manualmente: pip install -r requirements.txt
)

REM ── Crear carpetas necesarias ─────────────────────────────────
if not exist "projects"          mkdir projects
if not exist "exports"           mkdir exports
if not exist "assets"            mkdir assets
if not exist "templates\web"     mkdir templates\web
if not exist "templates\mobile"  mkdir templates\mobile
if not exist "templates\qa"      mkdir templates\qa
echo [OK] Carpetas de datos creadas.

echo.
echo ====================================================
echo   Setup completado exitosamente!
echo.
echo   Para ejecutar la aplicacion:
echo     run.bat
echo.
echo   Para compilar el ejecutable .exe:
echo     build_exe.bat
echo ====================================================
echo.
pause
