# Implementation Plan: PySwissShef StackBlitz Lab Configuration

This plan outlines the steps to configure the **PySwissShef** repository for a seamless, interactive experience on StackBlitz, addressing virtual environments, execution restrictions, and a unified entry point.

## Proposed Changes

### 1. Root Configuration (PySwissShef)

#### [NEW] [requirements.txt](file:///c:/AppDev/My_Linkdin/projects/iarxii/PySwissShef/requirements.txt)
Create a consolidated dependency list for the entire portfolio.
- **Includes**: `django`, `pandas`, `sqlalchemy`, `openpyxl`, `nltk`, `langdetect`, `googletrans`, `pyspellchecker`, `fpdf`.
- **Note**: `pyodbc` and `graphviz` will be categorized as "Extended Portability" and may be excluded from the base lab to avoid native binary errors in WebContainers.

#### [NEW] [main.py](file:///c:/AppDev/My_Linkdin/projects/iarxii/PySwissShef/main.py)
A unified entry point designed for both Web and CLI interactions.
- **Web Mode**: Bootstraps the environment (migrations, NLP data) and launches the Django development server.
- **CLI Mode**: Provides a minimal interactive menu with:
    - **Diagnostics**: `check-env` (lib audit, path verification, browser-env detection).
    - **Maintenance**: `reset-db` (confirmation-gated), `cleanup` (purge logs/cache), `sync-assets` (NLP data fetch).
    - **Execution**: Run automation scripts with safe defaults.
- **Safety Mechanisms**:
    - Confirms destructive actions.
    - Path isolation checks for script execution.
    - Global exception handling to prevent terminal crashes.

#### [NEW] [CLI_GUIDE.md](file:///c:/AppDev/My_Linkdin/projects/iarxii/PySwissShef/CLI_GUIDE.md)
Detailed documentation of CLI commands, diagnostics, and usage safety tips (to be located within the submodule).

#### [NEW] [.stackblitzrc](file:///c:/AppDev/My_Linkdin/projects/iarxii/PySwissShef/.stackblitzrc)
Standard configuration to automate the startup sequence.
- Sets the `startCommand` to `python main.py`.
- Enables automatic dependency installation.

### 2. Django Patching

#### [MODIFY] [views.py](file:///c:/AppDev/My_Linkdin/projects/iarxii/PySwissShef/automation_portfolio/scripts/views.py)
Update the `subprocess` logic to be environment-aware.
- Use `sys.executable` instead of the hardcoded `"python"` string to ensure the script runs accurately within the active virtual environment or WebContainer.

---

## User Review Required

> [!IMPORTANT]
> **Native Extensions**: StackBlitz WebContainers currently have limited support for native drivers (like `pyodbc` for MSSQL). I will configure the lab to skip MSSQL tests by default to prevent boot errors, focuses instead on the Data/NLP automation suites.

> [!NOTE]
> **Virtual Environment**: StackBlitz automatically manages a Node-based WebContainer environment for Python. While I will include `venv` logic in `main.py` for local users, the Lab experience will rely on the pre-installed container environment for maximum speed.

## Verification Plan

### Automated Tests
- Run `python main.py` in the terminal to verify the CLI menu appears.
- Run `python main.py --web` to verify Django boots and serves the portal.

### Manual Verification
- Verify the "Launch Lab Console" bridge in the Adaptivconcept portfolio leads correctly to the configured repo.
- Test the "Sentiment Analysis" script through the portal to ensure `nltk` data was downloaded correctly.
