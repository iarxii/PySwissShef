# 🛠️ PySwissShef CLI & Lab Guide

Welcome to the **PySwissShef** technical portal. This guide details the CLI commands and safety mechanisms available within the lab environment.

## 🚀 Getting Started

To launch the unified entry point, run:
```bash
python main.py
```

## 📋 Available Commands

| Command | Action | Description |
| :--- | :--- | :--- |
| `web` | `python main.py --web` | Launches the Django automation portal on port 8000. |
| `check-env` | `python main.py --check` | Performs a diagnostic audit of dependencies and lexicons. |
| `reset-db` | `python main.py --reset` | **Destructive**: Re-initializes the SQLite database. |
| `cleanup` | `python main.py --cleanup` | Removes temporary logs, caches, and output files. |
| `sync-assets` | `python main.py --sync` | Downloads necessary NLP assets (NLTK VADER lexicons). |

## 🛡️ Safety Mechanisms

- **Confirmation Gating**: Actions like `reset-db` will prompt for confirmation before proceeding.
- **Dependency Guard**: The system checks for "Native" dependencies (like `graphviz` or `pyodbc`). If missing, related features are gracefully disabled instead of crashing.
- **Path Isolation**: Script execution is confined to the specific automation folders to protect repository integrity.
- **Environment Detection**: Detects if running in a **StackBlitz WebContainer** and adjusts resource allocation accordingly.

## 🧪 Advanced Usage (Docker)

If you have Docker installed and need the **full** suite of native drivers (including MSSQL/Graphviz), use the provided configuration:
```bash
docker-compose up --build
```

---
> [!IMPORTANT]
> In StackBlitz environments, some native features (MSSQL analysis, PDF generation via native libs) may be restricted. Use the `check-env` command to verify capability status.
