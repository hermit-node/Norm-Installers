@echo off
setlocal EnableExtensions
cd /d "%~dp0" || exit /b 1

if exist "%~dp0Norm-Installer.exe" goto :compiled
where py >nul 2>nul
if errorlevel 1 goto :python
py -3.14 "%~dp0Norm-Installer.py" %*
exit /b %errorlevel%

:python
python "%~dp0Norm-Installer.py" %*
exit /b %errorlevel%

:compiled
"%~dp0Norm-Installer.exe" %*
exit /b %errorlevel%
