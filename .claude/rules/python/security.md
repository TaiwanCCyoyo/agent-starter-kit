---
paths:
    - "**/*.py"
    - "**/*.pyi"
---

# Python Security

## Secret Management

Use `os.environ["NAME"]` or the application's existing configuration layer for required secrets. Do not add a dotenv dependency unless the project explicitly adopts one.

Add a security scanner only when it is installed and configured as a repository dependency or CI gate.
