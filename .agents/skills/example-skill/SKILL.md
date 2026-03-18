---
name: verify-http-health
description: A basic skill to check if a local HTTP server is responding correctly.
---
# Verify HTTP Health Skill

## Intent
Use this skill to quickly ping a local service and confirm it returns a 200 OK status. 

## Requirements
- `curl` must be installed.

## Usage
Run the following script via shell execution to verify the service:
```bash
curl -I http://localhost:PORT
```
If the status code is 200, the verification is successful. Otherwise, report the error.
