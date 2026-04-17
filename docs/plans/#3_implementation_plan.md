# Implementation Plan: StackBlitz Compatibility & In-Process Execution

This plan addresses the `ModuleNotFoundError: No module named '_signal'` encountered in StackBlitz WebContainers by refactoring the **PySwissShef** entry points to avoid the `subprocess` module.

## The Problem: WASM vs Subprocess
The Python runtime in StackBlitz uses WebAssembly (WASM), which does not support the low-level signal and forking architecture required by the `subprocess` module.

## Proposed Changes

### 1. Refactor Entry Point: `main.py`

#### [MODIFY] [main.py](file:///c:/AppDev\My_Linkdin\projects\iarxii\PySwissShef\main.py)
- Replace all `subprocess.run` calls with functional equivalents.
- For `run_web()`: Instead of spawning `python manage.py runserver`, we will use Django's internal management tools:
  ```python
  from django.core.management import execute_from_command_line
  execute_from_command_line([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
  ```
- For `migrate`: Use `execute_from_command_line([sys.executable, "manage.py", "migrate"])`.

### 2. Refactor Script Execution: `views.py`

#### [MODIFY] [views.py](file:///c:/AppDev\My_Linkdin\projects\iarxii\PySwissShef\automation_portfolio\scripts\views.py)
- Implement a fallback execution engine using `runpy` (standard Python library).
- When a script is launched, we will attempt to execute it in-process:
  ```python
  import runpy
  # This runs the script file's code within the current process
  runpy.run_path(script.script_file.path, run_name="__main__")
  ```
- **Note**: This will require capturing `stdout` via `io.StringIO` since we can't capture it from a subprocess pipe.

### 3. Handle Git Submodule Warning
- **Explanation**: Acknowledge that StackBlitz WebContainers do not support the Git submodule protocol.
- **Guidance**: For StackBlitz use, we will recommend a "Flat" branch where submodules are included as regular directories.

---

## User Review Required

> [!IMPORTANT]
> **In-Process Risks**: Running scripts in-process means a crash in a script (like an `exit()`) could kill the entire web server. I will implement a safety wrapper using `try/except` and `contextlib.redirect_stdout`.

> [!WARNING]
> **Signal Failure**: Some heavy-duty Python libraries (like certain versions of `multiprocessing`) may still fail in StackBlitz even with these fixes. This reinforces the **"Replit/Codespaces Recommended"** badging.

## Verification Plan

### Automated Tests
- Test `main.py` locally to ensure it still launches the server correctly.
- Test script execution using `runpy` fallback.

### Manual Verification
- Re-test the updated code in the StackBlitz environment.
