@echo off
title AI Watermark Remover Launcher
cd /d "%~dp0"

echo Checking system requirements...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not added to your PATH!
    echo Please install Python 3.10 or higher from python.org.
    echo IMPORTANT: Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ===================================================
    echo First-time setup detected!
    echo Creating virtual environment and installing AI libraries...
    echo This may take a few minutes depending on your connection.
    echo Please do not close this window!
    echo ===================================================
    echo.
    
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo.
    echo Setup complete! Starting application...
) else (
    call venv\Scripts\activate.bat
)

:: Launch the application silently and close this terminal
start "" pythonw gui_app.py
exit
