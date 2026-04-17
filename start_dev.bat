@echo off
setlocal
echo [🔧] PySwissShef Local Dispatcher
echo.

REM Check for venv
if exist ".venv\Scripts\activate.bat" (
    echo [OK] Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo [OK] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found. Running with system python.
)

echo [🌐] Preparing Lab Portal...
echo [!] Note: Browser will launch in 5 seconds to give the server a head-start.
timeout /t 5 /nobreak > nul
start "" "http://127.0.0.1:8000"
python main.py --web

pause
