@echo off
echo ===================================================
echo Starting AeroReserve Django Development Server...
echo ===================================================
if not exist venv (
    echo [ERROR] Virtual environment 'venv' not found in the root directory.
    echo Please make sure the 'venv' directory exists.
    pause
    exit /b 1
)
venv\Scripts\python Scripts\manage.py runserver
