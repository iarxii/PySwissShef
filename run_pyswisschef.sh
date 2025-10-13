#!/bin/bash

# Activate virtual environment
source .venv/Scripts/activate

# Navigate to Django project directory
cd automation_portfolio

# Check for -m flag
if [ "$1" == "-m" ]; then
    echo "Running migrations..."
    python manage.py makemigrations
    python manage.py migrate
fi

# Run Django development server
python manage.py runserver
"""

# Save the updated script
with open("run_pyswisschef.sh", "w") as f:
    f.write(bash_script)

print("run_pyswisschef.sh script has been updated to support -m flag for migrations.")