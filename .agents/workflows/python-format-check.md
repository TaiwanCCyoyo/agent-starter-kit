---
description: Check Python code formatting and linting (autopep8, isort, flake8) for the whole project or modified files only, with venv support.
---

# Python Format Check

This workflow is used to quickly format and check Python files for a project using `autopep8`, `isort`, and `flake8`. It prioritizes project-local virtual environments (`venv`, `.venv`).

## 1. Check Entire Project
Run these commands to format and check all Python files in the current project.

### PowerShell (Windows)
// turbo
```powershell
$env:PYTHONUTF8=1; $python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } elseif (Test-Path "venv\Scripts\python.exe") { "venv\Scripts\python.exe" } else { "python" }; & $python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 --recursive .; & $python -m isort .; & $python -m flake8 --max-line-length=120 .
```

### Bash (macOS/Linux)
// turbo
```bash
if [ -d ".venv" ]; then python=".venv/bin/python"; elif [ -d "venv" ]; then python="venv/bin/python"; else python="python"; fi; $python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 --recursive . && $python -m isort . && $python -m flake8 --max-line-length=120 .
```

---

## 2. Check Modified Files Only
Run these commands to format and check only the Python files that have been modified (based on `git status`).

### PowerShell (Windows)
// turbo
```powershell
$env:PYTHONUTF8=1; $python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } elseif (Test-Path "venv\Scripts\python.exe") { "venv\Scripts\python.exe" } else { "python" }; $changedFiles = git status --porcelain | where { $_ -match '\.py$' } | foreach { $_.Substring(3) }; if ($changedFiles) { & $python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 $changedFiles; & $python -m isort $changedFiles; & $python -m flake8 --max-line-length=120 $changedFiles } else { Write-Host "No modified Python files found." }
```

### Bash (macOS/Linux)
// turbo
```bash
if [ -d ".venv" ]; then python=".venv/bin/python"; elif [ -d "venv" ]; then python="venv/bin/python"; else python="python"; fi; files=$(git status --porcelain | grep '\.py$' | cut -c4-); if [ -n "$files" ]; then $python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 $files && $python -m isort $files && $python -m flake8 --max-line-length=120 $files; else echo "No modified Python files found."; fi
```

---

## 3. Auto-Fix Formatting Only
If you only want to run the formatters without a linting check:

// turbo
```powershell
$env:PYTHONUTF8=1; $python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }; & $python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 .; & $python -m isort .
```

__Note__: If a line exceeds line-length and cannot be broken nicely (like a URL), append `# noqa: E501` to the end of the line.
