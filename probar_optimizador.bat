@echo off
cd /d "%~dp0"
title PRUEBA corta del optimizador
".venv\Scripts\python.exe" scripts\optimizer.py --prueba
pause
