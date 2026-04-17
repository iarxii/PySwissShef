from django.shortcuts import render, get_object_or_404
from .models import AutomationScript
import runpy
import io
import contextlib
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

def script_detail(request, script_id):
    script = get_object_or_404(AutomationScript, id=script_id)
    return render(request, 'script_detail.html', {'script': script})

def run_script(request, script_id):
    script = get_object_or_404(AutomationScript, id=script_id)
    
    # Capture output buffer
    f = io.StringIO()
    error_msg = ""
    
    try:
        with contextlib.redirect_stdout(f):
            # In-process execution via runpy
            runpy.run_path(script.script_file.path, run_name="__main__")
    except SystemExit:
        # Prevent script exit() from killing the server
        pass
    except Exception as e:
        error_msg = str(e)
    
    output = f.getvalue()
    
    # Return to details page with results
    return render(request, 'script_detail.html', {
        'script': script, 
        'output': output, 
        'error': error_msg
    })