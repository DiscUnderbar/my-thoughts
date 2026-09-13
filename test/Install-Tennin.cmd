@echo off
setlocal

set "COMPILER=%~dp0build\tenn.exe"
if not exist "%COMPILER%" (
  echo Tennin compiler was not found: "%COMPILER%"
  echo Build the project first, then run this installer again.
  pause
  exit /b 1
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Compiler "%COMPILER%"
if errorlevel 1 (
  echo Installation failed.
  pause
  exit /b 1
)

echo.
echo Tennin installation completed. Open a new PowerShell window and run: tenn program.tenn
pause
