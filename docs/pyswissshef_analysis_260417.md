# Technical Analysis: PySwissShef StackBlitz Readiness

This document analyzes the current state of the **PySwissShef** repository and outlines the configuration requirements for a high-fidelity StackBlitz "Lab" deployment.

## 🏗️ Architectural Overview

- **Core Framework**: Django 5.2.7 (Python-based monolith).
- **Database Layer**: SQLite (`db.sqlite3`), perfectly suited for browser-based WebContainers.
- **Execution Model**: The platform acts as a "Script Runner". It executes child processes via `subprocess.run` to run automation tasks (Data Processing, Sentiment Analysis, SQL Tools).
- **Frontend**: Django Templates with a custom stylized UI (Glassmorphic tendencies observed in `templates`).

## 📦 Dependency Matrix

Based on source code analysis, the following libraries are required:

| Component | Library | Purpose |
| :-- | :-- | :-- |
| **Web** | `django` | Core framework |
| **Data** | `pandas`, `openpyxl` | Excel and CSV manipulation |
| **DB** | `sqlalchemy` | SQL-level automation and migration |
| **ML/NLP** | `nltk`, `langdetect` | Sentiment analysis and language detection |
| **Utility** | `googletrans`, `pyspellchecker` | Translation and spell checking |

> [!WARNING]
> **NLTK Data**: Scripts using `nltk.SentimentIntensityAnalyzer` require the `vader_lexicon` data package. This must be downloaded during the container boot process.

## ⚡ StackBlitz Adaptation Strategy

To ensure a seamless "One-Click" experience in StackBlitz WebContainers, the following configurations are necessary:

### 1. Project Entry Point (`main.py`)
A root-level `main.py` should be created to act as a diagnostic and bootstrapper. It will:
- Verify the Python environment.
- Initialize the SQLite database (apply migrations).
- Download necessary NLP lexicons.
- Start the Django development server.

### 2. StackBlitz Configuration (`.stackblitzrc`)
A configuration file to automate the startup sequence:
```json
{
  "startCommand": "python main.py",
  "installDependencies": true,
  "env": {
    "PYTHONUNBUFFERED": "1"
  }
}
```

### 3. Subprocess Compatibility
The current implementation in `views.py` uses `subprocess.run(['python', ...])`. In some WebContainer environments, `python3` is the preferred alias. 
> [!TIP]
> Recommendation: Update `views.py` to use `sys.executable` instead of the literal string `'python'` to ensure portability across local and lab environments.

## 🛠️ Recommended Action Items

1. [ ] **Generate `requirements.txt`**: Create a comprehensive dependency list at the root.
2. [ ] **Implement `main.py` Bootstrapper**: Handle migrations and lexicon downloads.
3. [ ] **Add `.stackblitzrc`**: Automate the lab boot process.
4. [ ] **Patch `views.py`**: Ensure subprocess calls are environment-agnostic.
