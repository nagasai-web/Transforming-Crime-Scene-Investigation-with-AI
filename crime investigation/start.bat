@echo off
echo ========================================
echo AI Crime Detection System - Quick Start
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [4/5] Installing dependencies...
pip install -r requirements.txt
echo.

echo [5/5] Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Starting Django server...
echo Access the application at: http://127.0.0.1:8000/
echo.
echo Admin Login:
echo   URL: http://127.0.0.1:8000/admin-login/
echo   Username: admin
echo   Password: admin
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
