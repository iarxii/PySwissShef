# The Chef's Guide to Laboratory Stations

Welcome to the **PySwissShef Laboratory**. To ensure the highest precision for our automation recipes, we provide several "Stations" optimized for different levels of heat and dependency.

## 🍧 Station 1: The Tasting Room (StackBlitz)
**Best For**: UI Exploration, Recipe Browsing, "Light" Python standard library scripts.
- **Environment**: WebAssembly (WASM) in-browser container.
- **Pros**: Lightning fast, one-click share, zero setup.
- **Cons**: No `pip` support (cannot install new libraries), no `subprocess` (cannot fork processes).
- **Usage**: Perfect for showing your portfolio UI and basic logic.

## 🥘 Station 2: The High-Heat Kitchen (Replit)
**Best For**: **Full Execution**, Subprocesses, Django Backend, Data Processing.
- **Environment**: Dedicated Linux VM.
- **Pros**: Full terminal support, installs all `requirements.txt`, stays alive in the background.
- **Cons**: May require a Replit account for the best persistent storage.
- **Usage**: The primary destination for a working demo of "Heavy" automation tools.

## 🧪 Station 3: The Pro Lab (GitHub Codespaces)
**Best For**: Development, Customization, Heavy Data Science.
- **Environment**: Full VS Code in the browser with a powerful Linux VM.
- **Pros**: 60 hours/month free, full Docker support, professional IDE experience.
- **Cons**: Requires a GitHub account.
- **Usage**: The ultimate choice for a deep-dive into the codebase and heavy automation testing.

## 🏡 Station 4: The Home Chef (Local Workstation)
**Best For**: Privacy, Performance, Local Filesystem Automation.
- **Environment**: Your personal Windows/Linux/Mac machine.
- **Pros**: Fastest performance, no cloud limits, full access to local files and drivers.
- **Cons**: Requires manual Python installation.
- **Usage**: Running the tools on your own real-world data securely.

---

> [!TIP]
> **Check the Recipe!** Each script in the Lab is badged with it's recommended environment. If you see "Heavy," head over to the **High-Heat Kitchen (Replit)**!
