@echo off
chcp 65001 >nul
title Documentador de Proyectos

if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
    pythonw main.py
) else (
    python main.py
)
