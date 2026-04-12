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

## 1. Project-wide Hygiene & Auto-Fix
Run this command to format the code and fix auto-fixable lint errors across the entire project. This script captures and displays any errors that cannot be fixed automatically.

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uv run python scripts/auto_format.py
```

---

## 2. Check Specific Files/Directories
You can also target specific paths. You can view all available options using the `--help` flag.

### PowerShell (Windows) / Bash (macOS/Linux)
// turbo
```powershell
uv run python scripts/auto_format.py --help
uv run python scripts/auto_format.py scripts/ some_file.py
```

> [!NOTE]
> The `--hook` flag is reserved for internal use by the Gemini AI agent and should not be used in manual CLI execution.


__Note__: If a line exceeds line-length and cannot be broken nicely, append `# noqa: E501` to the end of the line to suppress the Ruff warning.
