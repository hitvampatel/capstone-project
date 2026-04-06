@echo off
echo ============================================
echo  Karnavati University Event Registration
echo ============================================
echo.
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python from https://python.org
    pause
    exit /b 1
)
echo Installing Flask if needed...
pip install flask --quiet
echo.
echo Starting server...
echo Open your browser at: http://localhost:5000
echo Admin panel at:       http://localhost:5000/admin
echo.
echo Press Ctrl+C to stop the server.
echo.
cd /d "%~dp0"
python app.py
pause
