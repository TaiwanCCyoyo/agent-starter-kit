---
name: security-scanner
description: A robust credential scanner that detects secrets. It prefers gitleaks if installed, and falls back to a high-entropy regex scan if gitleaks is missing.
---
# Security Scanner Skill

## Intent
To prevent any API keys, passwords, or sensitive credentials from being committed to the repository.

## Logic Overview
1. **Check for Gitleaks**: Executed via shell. If available, run `gitleaks detect --staged --verbose`.
2. **Fallback Scan**: If `gitleaks` is NOT found in the system PATH, run a series of `grep` or `Select-String` (PowerShell) patterns to catch major API key formats:
   - OpenAI: `sk-[a-zA-Z0-9]{48}`
   - Google AI: `AIza[0-9A-Za-z-_]{35}`
   - generic AWS: `AKIA[0-9A-Z]{16}`
   - Common Token Patterns: `[A-Za-z0-9-_]{32,}` (Filtered to avoid common collisions)

## Usage Instruction for Agent
Always run this skill as the first step of your `PRE_COMMIT_SOP.md`. 
- **If it passes**: Proceed to commit.
- **If it fails**: Report the exact leaked content and block the commit.
- **If it falls back to Regex**: Log a warning reminding the human to install `gitleaks` for better security.

## Script Implementation (PowerShell Fallback)
```powershell
if (Get-Command gitleaks -ErrorAction SilentlyContinue) {
    gitleaks detect --staged --verbose
} else {
    Write-Host "WARNING: Gitleaks not found. Using Fallback Regex Scan..." -ForegroundColor Yellow
    $staged_diff = git diff --staged
    $patterns = 'AIza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{48}|AKIA[0-9A-Z]{16}'
    $matches = $staged_diff | Select-String -Pattern $patterns
    if ($matches) {
        Write-Error "CRITICAL: Potential secrets detected in staged changes!`n$matches"
        exit 1
    } else {
        Write-Host "Fallback scan: No obvious secrets detected." -ForegroundColor Green
    }
}
```
