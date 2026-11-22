@echo off
chcp 65001 >nul
title Optimizador del soporte MSD
cd /d "%~dp0"
echo.
echo  Arrancando el optimizador... (se puede cerrar esta ventana cuando quieras;
echo  al volver a abrirla continua exactamente donde iba)
echo.
:bucle
".venv\Scripts\python.exe" scripts\optimizer.py
set CODIGO=%ERRORLEVEL%
if "%CODIGO%"=="0" goto fin
if "%CODIGO%"=="2" goto fin
if "%CODIGO%"=="3" goto fin
echo.
echo  El optimizador se ha detenido por un error (codigo %CODIGO%). Se reinicia solo en 60 segundos...
echo  (cierra esta ventana si no quieres que se reinicie)
timeout /t 60 /nobreak >nul
goto bucle
:fin
echo.
echo  El optimizador se ha detenido. Pulsa una tecla para cerrar esta ventana.
pause >nul
