---
description: Check Python code formatting and linting using Ruff (`uvx ruff`) for the whole project or modified files.
---

# Python Format Check (Ruff)

This workflow uses `ruff` (via `uv`) as the unified Python linter and formatter. 

**Prerequisites**: This script relies on `uv` being installed and used as the package manager in this project.

## 1. Format and Fix Entire Project
Run these commands to automatically format the code and fix auto-fixable lint errors across all Python files in the current project.

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uvx ruff check --fix .; uvx ruff format .
```

---

## 2. Check Modified Files Only
Run these commands to format and check only the Python files that have been modified (based on `git status`).

### PowerShell (Windows)
// turbo
```powershell
$changedFiles = git status --porcelain | where { $_ -match '\.py$' } | foreach { $_.Substring(3) }; if ($changedFiles) { uvx ruff check --fix $changedFiles; uvx ruff format $changedFiles } else { Write-Host "No modified Python files found." }
```

### Bash (macOS/Linux)
// turbo
```bash
files=$(git status --porcelain | grep '\.py$' | cut -c4-); if [ -n "$files" ]; then uvx ruff check --fix $files && uvx ruff format $files; else echo "No modified Python files found."; fi
```

---

## 3. Check Only (No Auto-Fix)
If you only want to see what's wrong without changing the files automatically (e.g. CI checks):

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uvx ruff check .; uvx ruff format --check .
```

__Note__: If a line exceeds line-length and cannot be broken nicely, append `# noqa: E501` to the end of the line to suppress the Ruff warning.
