import os
import sys
import subprocess
import shutil
import platform
import argparse

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DJANGO_DIR = os.path.join(PROJECT_ROOT, "automation_portfolio")
DB_PATH = os.path.join(DJANGO_DIR, "db.sqlite3")

def print_banner():
    banner = r"""
    PySwissShef
    -----------
    >>> Lab Portal & Automation Toolkit <<<
    """
    print(banner)

def run_command(cmd, cwd=None, shell=False):
    """Utility to run shell commands and capture errors."""
    try:
        subprocess.run(cmd, cwd=cwd, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        print(f"Exit Code: {e.returncode}")
        return False

def check_environment():
    """Diagnostic check for dependencies and environment health."""
    print("\n[+] Performing System Diagnostics...")
    
    # 1. Python Version
    print(f"Python Integrity: {sys.version.split()[0]} ({platform.system()})")
    
    # 2. Dependency Audit
    libs = [
        ('django', 'Django (Web)'),
        ('pandas', 'Pandas (Data)'),
        ('nltk', 'NLTK (NLP)'),
        ('langdetect', 'LangDetect'),
        ('googletrans', 'GoogleTrans'),
        ('fpdf', 'FPDF (Reporting)')
    ]
    
    for lib, display in libs:
        try:
            __import__(lib)
            print(f"  [OK] {display}")
        except ImportError:
            print(f"  [!!] {display} is NOT installed")

    # 3. Native Drivers (Informative)
    try:
        import pyodbc
        print("  [OK] pyodbc (MSSQL Support)")
    except ImportError:
        print("  [--] pyodbc (MSSQL) - Limited (Native driver missing, common in Lab environments)")

    # 4. Lexicon Check
    nltk_data_path = os.path.expanduser('~/nltk_data/sentiment/vader_lexicon.zip')
    if os.path.exists(nltk_data_path):
        print("  [OK] NLTK Vader Lexicon present")
    else:
        print("  [--] NLTK Vader Lexicon missing (Run --sync to fix)")

    print("\nDiagnostics complete.")

def sync_assets():
    """Download required assets like NLTK data."""
    print("\n[+] Syncing Laboratory Assets...")
    try:
        import nltk
        nltk.download('vader_lexicon')
        print("Asset sync finalized.")
    except Exception as e:
        print(f"Sync failed: {e}")

def reset_database():
    """Reset the SQLite database."""
    confirm = input("\n[!] DANGER: This will wipe all current Lab data. Proceed? (y/N): ")
    if confirm.lower() == 'y':
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("Dropped existing database.")
        
        print("Initializing fresh database...")
        os.chdir(DJANGO_DIR)
        run_command([sys.executable, "manage.py", "migrate"])
        print("Re-initialized database.")
    else:
        print("Reset aborted.")

def run_web():
    """Start the Django Portal."""
    print("\n[+] Starting Web Portal...")
    # Ensure migrations are done
    os.chdir(DJANGO_DIR)
    run_command([sys.executable, "manage.py", "migrate"])
    
    # Launch server
    try:
        subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\nWeb Portal stopped.")

def cleanup():
    """Clean caches and logs."""
    print("\n[+] Cleaning Laboratory...")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
        for f in files:
            if f.endswith(".pyc") or f == "error_debug.txt":
                os.remove(os.path.join(root, f))
    print("Cleanup complete.")

def main():
    parser = argparse.ArgumentParser(description="PySwissShef Unified Entry Point")
    parser.add_argument("--web", action="store_true", help="Launch the Web Portal")
    parser.add_argument("--check", action="store_true", help="Run System Diagnostics")
    parser.add_argument("--reset", action="store_true", help="Reset the Laboratory Database")
    parser.add_argument("--sync", action="store_true", help="Sync required Lab assets")
    parser.add_argument("--cleanup", action="store_true", help="Clean caches and temporary files")
    
    args = parser.parse_args()

    print_banner()

    if args.web:
        run_web()
    elif args.check:
        check_environment()
    elif args.reset:
        reset_database()
    elif args.sync:
        sync_assets()
    elif args.cleanup:
        cleanup()
    else:
        # Interactive Menu
        while True:
            print("\n--- Lab Control Menu ---")
            print("1. Launch Web Portal (--web)")
            print("2. Run Diagnostics (--check)")
            print("3. Sync Assets (--sync)")
            print("4. Reset Laboratory (--reset)")
            print("5. Cleanup Environment (--cleanup)")
            print("q. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '1': run_web()
            elif choice == '2': check_environment()
            elif choice == '3': sync_assets()
            elif choice == '4': reset_database()
            elif choice == '5': cleanup()
            elif choice.lower() == 'q':
                print("Exiting Lab.")
                break
            else:
                print("Invalid selection.")

if __name__ == "__main__":
    main()
