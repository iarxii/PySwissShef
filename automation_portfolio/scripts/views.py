from django.shortcuts import render
from .models import AutomationScript
import subprocess
import sys

def home(request):
    scripts = AutomationScript.objects.all()
    return render(request, 'home.html', {'scripts': scripts})

def automation_showcase(request):
    category = request.GET.get('category')
    if category:
        scripts = AutomationScript.objects.filter(category=category)
    else:
        scripts = AutomationScript.objects.all()
    return render(request, 'automation_showcase.html', {'scripts': scripts, 'selected_category': category})

def myprofile(request):
    scripts = AutomationScript.objects.all()
    return render(request, 'myprofile.html', {'scripts': scripts})

def contact(request):
    scripts = AutomationScript.objects.all()
    return render(request, 'contact.html', {'scripts': scripts})


def run_script(request, script_id):
    script = AutomationScript.objects.get(id=script_id)
    result = subprocess.run([sys.executable, script.script_file.path], capture_output=True, text=True)
    return render(request, 'home.html', {'scripts': AutomationScript.objects.all(), 'output': result.stdout})