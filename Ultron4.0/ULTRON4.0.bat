@echo off
cls
title ULTRON 4.0
color 4
cd /d "%~dp0"
call .venv\Scripts\activate
"%~dp0.venv\Scripts\python.exe" Ultron4.0.py
pause