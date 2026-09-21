@echo off
echo ========================================
echo Gemini AI Integration Setup
echo ========================================
echo.

echo [1/4] Installing Google Generative AI library...
pip install google-generativeai==0.3.2
if errorlevel 1 (
    echo ERROR: Failed to install google-generativeai
    pause
    exit /b 1
)
echo.

echo [2/4] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo.

echo [3/4] Checking installation...
python -c "import google.generativeai as genai; print('✓ Google Generative AI installed successfully')"
if errorlevel 1 (
    echo ERROR: Import failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Get your Gemini API key from: https://aistudio.google.com/apikey
echo 2. Start server: python manage.py runserver
echo 3. Login as admin: http://127.0.0.1:8000/admin-login/
echo 4. Go to "Gemini AI Configuration"
echo 5. Enter your API key and save
echo.
echo Admin credentials:
echo   Username: admin
echo   Password: admin
echo.
pause
