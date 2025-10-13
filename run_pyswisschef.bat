REM Windows-compatible .bat script to run the Django app with optional migrations
@echo off

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Navigate to Django project directory
cd automation_portfolio

REM Check for -m flag
IF "%1"=="-m" (
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate
)

REM Run Django development server
python manage.py runserver
"""

# Save the script to a .bat file
with open("run_pyswisschef.bat", "w") as f:
    f.write(bat_script)

print("run_pyswisschef.bat script has been created successfully.")