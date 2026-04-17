# Implementation Plan: Laboratory Code Vault Integration

This plan adds a professional, editor-style code preview window to the Laboratory's detail pages, enabling users to "inspect the ingredients" (source code) of each recipe without leaving the portal.

## Proposed Changes

### 1. Data & Asset Orchestration

#### [NEW] `src/data/raw_scripts/`
- Establish a dedicated directory in the React source to house the "Gourmet Scripts" as raw assets for the bundler.

#### [ORCHESTRATION]
- Copy the 4 verified Python scripts from the Django `scripts/` directory into this new folder. This ensures they are available to Vite's asset pipeline via `?raw` imports.

### 2. Component Development

#### [NEW] `src/components/CodeVault.jsx`
- **Aesthetic**: Premium "Midnight Console" theme with gold borders.
- **Features**: 
  - JetBrains Mono typography.
  - Sidebar line numbering.
  - "Copy Code" button with hover feedback.
  - Full-width container with `max-height: 80vh`.

### 3. Detail Page Integration

#### [MODIFY] `src/pages/RecipeDetail.jsx`
- **Dynamic Loading**: Implement a `useCodeLoader` hook or logic to import the specific `.py` content based on the `recipe.file` name.
- **Layout Expansion**: Place the `CodeVault` panel at the bottom of the page, spanning the full width of the view, positioned below the split Story/Terminal section.

---

## User Review Required

> [!IMPORTANT]
> **Static vs. Dynamic**: The code shown in the preview will be a snapshot of the scripts at the time of the React build. Any future changes to the Django `.py` files will require a re-sync or a commit to the React source folder.

## Verification Plan

### Automated Tests
- Build verification (`npm run build`).

### Manual Verification
- Use the browser tool to verify:
  1. Each of the 4 scripts loads its correct Python source.
  2. The code window scrolls independently and respects the `80vh` height limit.
  3. The "Copy" functionality works as expected.
