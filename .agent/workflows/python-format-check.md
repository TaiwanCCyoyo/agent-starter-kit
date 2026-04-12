---
description: Check Python code formatting and linting using Ruff (`uv run ruff`) for the whole project.
---

# Python Format Check (Ruff)

This workflow uses `ruff` (via `uv`) as the unified Python linter and formatter. 

**Prerequisites**: This script relies on `uv` being installed and used as the package manager in this project.

## 🚀 0. Automatic Formatting (New!)
In this project, Python formatting is now **automatic** for AI agents.
- **Git Hooks**: Pre-commit hooks will automatically run `ruff --fix` and `ruff-format` before every commit.
- **Gemini Hooks**: Whenever an agent uses `write_file` or `replace` on a `.py` file, the `scripts/auto_format.py` hook is triggered to immediately format and fix the file.

---

## 1. Manual Cleanup (Entire Project)
Run these commands to manually format the code and fix auto-fixable lint errors across all Python files.

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uv run ruff check --fix .; uv run ruff format .
```

---

## 2. Check Only (No Auto-Fix)
If you only want to see what's wrong without changing the files automatically (e.g., for CI validation):

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uv run ruff check .; uv run ruff format --check .
```

__Note__: If a line exceeds line-length and cannot be broken nicely, append `# noqa: E501` to the end of the line to suppress the Ruff warning.
