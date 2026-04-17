import os
import sys
import shutil
import platform
import argparse

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DJANGO_DIR = os.path.join(PROJECT_ROOT, "automation_portfolio")

def print_banner():
    banner = r"""
    PySwissShef Laboratory
    ----------------------
    >>> Gourmet Automation & Portal <<<
    """
    print(banner)

def run_web():
    """Start the Django Portal with auto-bootstrapping."""
    print("\n[+] Initializing Web Portal...")
    
    # Delayed Import to avoid startup crash on missing dependencies
    try:
        import django
        from django.core.management import execute_from_command_line
    except ImportError:
        print("\n" + "!"*50)
        print("  CRITICAL: DJANGO NOT FOUND")
        print("!"*50)
        print("\nThis environment lacks the required backend dependencies.")
        print("This is common in restricted WASM environments like StackBlitz.")
        print("\n>>> SOLUTION:")
        print("1. RUN: bash setup_stackblitz.sh")
        print("2. OR USE REPLIT: https://replit.com/github/iarxii/PySwissShef")
        print("\nFor more details, see: docs/LAB_STATIONS.md")
        print("!"*50 + "\n")
        return

    # Migration Check
    print("[+] Applying database migrations...")
    os.chdir(DJANGO_DIR)
    try:
        execute_from_command_line([sys.executable, "manage.py", "migrate"])
    except Exception as e:
        print(f"[!!] Migrations failed: {e}")
    
    # Launch Server
    print("[+] Server is starting at http://127.0.0.1:8000")
    try:
        execute_from_command_line([sys.executable, "manage.py", "runserver", "0.0.0.0:8000", "--noreload"])
    except KeyboardInterrupt:
        print("\nWeb Portal stopped.")
    except Exception as e:
        print(f"\n[!!] Portal Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="PySwissShef Unified Entry Point")
    parser.add_argument("--web", action="store_true", help="Launch the Web Portal")
    parser.add_argument("--check", action="store_true", help="Run System Diagnostics")
    
    # ... other args ...
    
    args, unknown = parser.parse_known_args()

    print_banner()

    if args.web or "--web" in sys.argv:
        run_web()
    else:
        print("Usage: python main.py --web")
        print("\nHint: If you are in StackBlitz, run 'bash setup_stackblitz.sh' first.")

if __name__ == "__main__":
    main()
