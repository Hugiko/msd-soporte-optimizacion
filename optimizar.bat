@echo off
chcp 65001 >nul
title Optimizador del soporte MSD
cd /d "%~dp0"
echo.
echo  Arrancando el optimizador... (se puede cerrar esta ventana cuando quieras;
echo  al volver a abrirla continua exactamente donde iba)
echo.
".venv\Scripts\python.exe" scripts\optimizer.py
echo.
echo  El optimizador se ha detenido. Pulsa una tecla para cerrar esta ventana.
pause >nul
