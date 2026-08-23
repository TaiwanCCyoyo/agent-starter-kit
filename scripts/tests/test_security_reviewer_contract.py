from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REVIEWERS = (
    ROOT / ".claude" / "agents" / "security-reviewer.md",
    ROOT / ".codex" / "agents" / "security-reviewer.toml",
)

AGENT_INSTRUCTIONS = (
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".codex" / "AGENTS.md",
)

REQUIRED_CHECKS = (
    "secrets",
    "input validation",
    "sql injection",
    "command injection",
    "authentication",
    "authorization",
    "xss",
    "csrf",
    "rate limiting",
    "error messages",
    "dependencies",
    "permissions",
)


@pytest.mark.parametrize("reviewer_path", REVIEWERS, ids=lambda path: path.parent.name)
def test_security_reviewer_has_conditional_checklist(reviewer_path: Path) -> None:
    content = reviewer_path.read_text(encoding="utf-8").lower()

    assert "when applicable checklist" in content
    assert "only require controls that apply" in content
    for check in REQUIRED_CHECKS:
        assert check in content


@pytest.mark.parametrize(
    "instructions_path",
    AGENT_INSTRUCTIONS,
    ids=lambda path: path.name,
)
def test_agent_instructions_preserve_external_research_fallback(
    instructions_path: Path,
) -> None:
    content = instructions_path.read_text(encoding="utf-8")

    assert ("Search GitHub or package registries only when local patterns and primary documentation are insufficient.") in content
