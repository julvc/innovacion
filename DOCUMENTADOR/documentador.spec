# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec — Documentador de Proyectos v1.0
Genera carpeta dist/DocumentadorProyectos/ lista para distribuir.
"""

import os
from pathlib import Path

block_cipher = None
PROJ = Path(SPECPATH)

# ── Archivos de datos a empaquetar ──────────────────────────────
datas = [
    (str(PROJ / "templates"), "templates"),
    (str(PROJ / "assets"),    "assets"),
]

# Incluir icono PNG si existe
for _img in ["DF 500X500 BLANCO 1.png", "icon.png"]:
    _p = PROJ / _img
    if _p.is_file():
        datas.append((str(_p), "."))

# ── Analisis ─────────────────────────────────────────────────────
a = Analysis(
    [str(PROJ / "main.py")],
    pathex=[str(PROJ)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # Modulos del proyecto
        "wizard",
        "doc_generator",
        "project_manager",
        "section_templates",
        "ai_connector",
        # Exportacion
        "docx",
        "docx.oxml",
        "docx.oxml.ns",
        "docx.oxml.shared",
        "docx.shared",
        "docx.enum.text",
        "docx.enum.style",
        "markdown",
        "markdown.extensions",
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
        "fpdf",
        # IA
        "requests",
        "requests.adapters",
        "urllib3",
        # Keyring Windows
        "keyring",
        "keyring.backends",
        "keyring.backends.Windows",
        "keyring.backends.fail",
        "keyring.core",
        # Jinja2 (usado por fpdf2 internamente)
        "jinja2",
        "jinja2.ext",
        # Pillow (icono)
        "PIL",
        "PIL.Image",
        "PIL.ImageTk",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib", "numpy", "pandas", "scipy",
        "pytest", "IPython", "notebook",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Icono .ico si existe
_ico = str(PROJ / "assets" / "icon.ico")
_ico_arg = _ico if os.path.isfile(_ico) else None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="DocumentadorProyectos",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                   # sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_ico_arg,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="DocumentadorProyectos",
)
