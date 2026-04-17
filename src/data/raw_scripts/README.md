# PySwissShef: Raw Script Assets

This directory houses the raw Python source code utilized by the React-based "Code Vault" previewer.

## 🍱 Sync Protocol
> [!IMPORTANT]
> **SNAPSHOT NOTICE**: The scripts in this directory are static snapshots of the source files located in `/automation_portfolio/scripts/`. 

**The React Portal does NOT automatically detect changes in the Django backend folders.**

Whenever you modify a script in the Django backend, you MUST perform a manual sync to update the Laboratory's Code Vault:

```bash
# Sync Pattern
cp automation_portfolio/scripts/*.py src/data/raw_scripts/
```

Failure to re-sync will result in the "Tasting Room" showing outdated ingredients.
