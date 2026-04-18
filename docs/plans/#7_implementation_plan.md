# Implementation Plan: Gourmet Syntax Highlighting

This plan upgrades the Code Vault from plain-text viewing to a professional, high-fidelity Python syntax highlighting experience, calibrated to the PySwissShef design system.

## Proposed Changes

### 1. Library Integration

#### [NEW] Dependency
- `react-syntax-highlighter` (already installed) will be utilized as the core highlighting engine.

### 2. Component Refactoring

#### [MODIFY] `src/components/CodeVault.jsx`
- **Engine Swap**: Replace the standard `pre/div` content with the `Prism` highlighter component.
- **Theming**: Implement the `atomDark` or `vscDarkPlus` theme base, customized via CSS to inject Laboratory colors:
  - **Keywords** (`def`, `class`, `import`): Gold (`#ffd43b`).
  - **Strings**: Muted Emerald/Green.
  - **Comments**: Dimmed Silver.
- **Layout Consistency**: Ensure the new highlighter respects the `80vh` max-height and custom scrollbar styling of the Bistro shell.

### 3. Visual Calibration

#### [MODIFY] `src/index.css`
- Add override styles for the Prism engine to ensure 100% parity with the "Midnight-Gold" palette.

---

## User Review Required

> [!NOTE]
> **Performance**: `react-syntax-highlighter` uses a virtualized approach for large files, which will actually improve the scrolling smoothness for your longer automation scripts (like the 22kb `sentiment_analysis.py`).

## Verification Plan

### Automated Tests
- Build verification (`npm run build`).

### Manual Verification
- Use the browser tool to verify:
  1. Python keywords are highlighted in Gold.
  2. The code window maintains its centered, glass-panel layout.
  3. Scrolling remains performant on the largest script.
