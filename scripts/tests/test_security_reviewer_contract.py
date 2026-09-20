from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REVIEWERS = (
    ROOT / ".claude" / "agents" / "security-reviewer.md",
    ROOT / ".codex" / "agents" / "security-reviewer.toml",
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
