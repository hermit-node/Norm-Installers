@echo off
setlocal EnableExtensions
cd /d "%~dp0" || exit /b 1

where py >nul 2>nul
if errorlevel 1 goto :python

py -3.14 "%~dp0Build-Installer.py" %*
exit /b %errorlevel%

:python
python "%~dp0Build-Installer.py" %*
exit /b %errorlevel%
