# Implementation Plan: Script Details & Environment Targeting

This plan outlines the evolution of the **PySwissShef** portal into a high-fidelity "Laboratory Catalogue." We will implement a dedicated Details Screen, a session-managed security disclaimer, and "Smart Infrastructure" for handling heavy data via sample files.

## Proposed Changes

### 1. Security & Session Management

#### [MODIFY] [base.html](file:///c:/AppDev\My_Linkdin\projects\iarxii\PySwissShef\automation_portfolio\automation_portfolio\templates\base.html)
- Implement a **Glassmorphism Security Overlay** (Modal) that appears on first-time site entry.
- **JS Logic**: Use `localStorage` (`pyswissshef_disclaimer_accepted`) to ensure users only see and accept the disclaimer once. Persistent across sessions.

### 2. Database Schema Evolution (The "Sample Data" Engine)

#### [MODIFY] [models.py](file:///c:/AppDev\My_Linkdin\projects\iarxii\PySwissShef\automation_portfolio\scripts\models.py)
Add new fields to `AutomationScript`:
- `repo_url` & `release_url` (GitHub integration).
- `detailed_description` (Extended documentation).
- `environment_target` (ChoiceField): `StackBlitz`, `Codespaces`, `Replit`, `Local Recommended`.
- `has_sample_data` (BooleanField): Whether the script can run with pre-bundled sample files.
- `security_level` (ChoiceField): `Low-Impact (Utility)`, `High-Access (System)`, `Experimental`.

### 3. The "Gourmet Detail" Template & Logic

#### [NEW] [script_detail.html](file:///c:/AppDev\My_Linkdin\projects\iarxii\PySwissShef\automation_portfolio\automation_portfolio\templates\script_detail.html)
A premium layout incorporating the "Cyber-Bistro" design system:
- **Environment & Data Strategy**:
    - **Classification**: Scripts requiring heavy file uploads will be labeled **"Download Recommended"**.
    - **Sample Data Toggle**: If `has_sample_data` is true, provide a "Use Chef's Ingredients" toggle that automatically points the script to a pre-defined sample CSV/File in the `static/samples/` directory.
- **Action Bar**:
    - **[Download Reference]** (GitHub Releases).
    - **[Launch in Lab]** (Executes the code specifically with sample data if selected).

---

## User Review Required

> [!IMPORTANT]
> **WebContainer Uploads**: While WebContainers allow file uploads, it's often friction-heavy for users. I will favor the **"Use Sample Data"** approach for browser demos to keep the "Chef's Experience" smooth, only prompting for native downloads when high-performance or privacy is required.

---

## Verification Plan

### Automated Tests
- Verify `localStorage` persistence in the browser subagent.
- Validate the "Sample Data" routing logic.

### Manual Verification
- Test disclaimer behavior (Accept $\rightarrow$ Refresh $\rightarrow$ Verify disappearance).
- Confirm "Download Recommended" badge appears on heavy-data projects.

---

## User Review Required

> [!WARNING]
> **Existing Data**: Scripts without `repo_url` or `release_url` will show "Coming Soon" or disabled buttons to maintain the UI integrity.

## Verification Plan

### Automated Tests
- Verify URL routing for the new `/script/<id>/` path.
- Test script execution triggering from the details page.

### Manual Verification
- Navigating from Home $\rightarrow$ Details $\rightarrow$ Run.
- Verifying the GitHub external links open in new tabs.
