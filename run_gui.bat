@echo off
title AI Watermark Remover GUI
echo Starting AI Watermark ^& Metadata Remover GUI...

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. 
    echo Please make sure you have installed the project using:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b
)

:: Activate and run
call venv\Scripts\activate.bat
python gui_app.py
