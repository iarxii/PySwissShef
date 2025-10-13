from django.shortcuts import render
from .models import AutomationScript
import subprocess

def home(request):
    scripts = AutomationScript.objects.all()
    return render(request, 'home.html', {'scripts': scripts})

def run_script(request, script_id):
    script = AutomationScript.objects.get(id=script_id)
    result = subprocess.run(['python', script.script_file.path], capture_output=True, text=True)
    return render(request, 'home.html', {'scripts': AutomationScript.objects.all(), 'output': result.stdout})