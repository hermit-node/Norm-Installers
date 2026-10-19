@echo off
call "%~dp0Build-Installer.bat" %*
exit /b %errorlevel%
