# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(description="Delegate a task to a specialized Subagent role.")
    parser.add_argument("--role", required=True, help="The target role from TEAM.yaml (e.g. QA_Auditor)")
    parser.add_argument("--task", required=True, help="The specific task instruction")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent
    project_root = skill_dir.parents[2]
    team_yaml_path = skill_dir / "TEAM.yaml"
    memory_path = skill_dir.parents[1] / "memory" / "MEMORY.md"
    temp_dir = skill_dir.parents[1] / "temp"

    try:
        temp_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating temp directory: {e}")
        sys.exit(1)

    prompt_file = temp_dir / "task_prompt.md"

    if not team_yaml_path.exists():
        print(f"Error: TEAM.yaml not found at {team_yaml_path}")
        sys.exit(1)

    try:
        with open(team_yaml_path, "r", encoding="utf-8") as f:
            team_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing TEAM.yaml: {e}")
        sys.exit(1)

    roles = team_data.get("roles", {})
    if args.role not in roles:
        print(f"Error: Role '{args.role}' not defined in TEAM.yaml. Available roles: {list(roles.keys())}")
        sys.exit(1)

    role_info = roles[args.role]
    description = role_info.get("description", "No description provided.")
    permissions = role_info.get("permissions", [])
    category = role_info.get("category", "specialist")
    triggers = role_info.get("triggers", [])
    constraints = role_info.get("constraints", {})

    memory_content = ""
    if memory_path.exists():
        try:
            with open(memory_path, "r", encoding="utf-8") as f:
                memory_content = f.read()
        except BaseException:
            pass

    # Format triggers and constraints for the prompt
    triggers_md = "\n".join([f"- **{t.get('domain')}**: {t.get('condition')}" for t in triggers]) if triggers else "None"
    use_when_md = "\n".join([f"- {c}" for c in constraints.get("use_when", [])]) if constraints.get("use_when") else "Not specified"
    avoid_when_md = "\n".join([f"- {c}" for c in constraints.get("avoid_when", [])]) if constraints.get("avoid_when") else "Not specified"

    prompt = f"""You are acting as the {args.role} role.

## Your Role Identity
- **Category**: {category}
- **Description**: {description}

## Domain Triggers
{triggers_md}

## Your Operational Constraints [STRICT ENFORCEMENT]
### Preferred Scenarios (Use When):
{use_when_md}

### Prohibited Scenarios (Avoid When):
{avoid_when_md}

## Allowed Skills (Permissions)
You are restricted to using the following skills: {', '.join(permissions)}
(If "*" is listed, you may use any available skill). Do NOT hallucinate skills.

## Project Guardian Protocol & Memory
{memory_content}

## Your Task
{args.task}

## Handover Protocol [CRITICAL]
When you have finished your task, you MUST summarize your findings, what you modified,
and any open questions into a file located at `.agents/temp/handover.md`.
Do not just output to the console. You must explicitly create/overwrite that file. Once done, gracefully exit.
"""

    try:
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
    except Exception as e:
        print(f"Error writing prompt file: {e}")
        sys.exit(1)

    print(f"Delegating task to {args.role}. Prompt written to {prompt_file.relative_to(project_root)}")
    print(f"Executing: gemini -p {prompt_file.relative_to(project_root)}")

    import os

    # On Windows, running batch/cmd wrapper scripts requires shell=True
    use_shell = os.name == 'nt'
    subprocess.run(["gemini", "-p", str(prompt_file)], shell=use_shell)


if __name__ == "__main__":
    main()
