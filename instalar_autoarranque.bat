@echo off
cd /d "%~dp0"
schtasks /Create /TN "MSD optimizador soporte" /TR "\"%~dp0optimizar.bat\"" /SC ONLOGON /RL LIMITED /F
echo.
echo  Listo: el optimizador se abrira solo cada vez que inicies sesion en Windows.
echo  (para quitarlo: desinstalar_autoarranque.bat)
pause
