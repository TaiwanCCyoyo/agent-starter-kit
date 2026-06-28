from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSION_HOOKS = (
    ROOT / ".agent" / "hooks" / "session_start.py",
    ROOT / ".claude" / "hooks" / "session_start.py",
    ROOT / ".codex" / "hooks" / "session_start.py",
)


def test_ruff_uses_inline_e402_suppression_for_session_hook_bootstrap() -> None:
    ruff_config = (ROOT / "ruff.toml").read_text(encoding="utf-8")

    assert "[lint.per-file-ignores]" not in ruff_config
    assert "E402" not in ruff_config

    for hook_path in SESSION_HOOKS:
        hook_content = hook_path.read_text(encoding="utf-8")

        assert "from scripts.memory_store import initialize_memory_store  # noqa: E402" in hook_content


def test_claude_instructions_use_direct_openspec_routing() -> None:
    claude_instructions = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert ("downstream" + " project") not in claude_instructions.lower()
    assert "Use OpenSpec to communicate plans and specs across agents" in claude_instructions


def test_codex_instructions_end_with_marked_karpathy_condensed_section() -> None:
    codex_instructions = (ROOT / ".codex" / "AGENTS.md").read_text(encoding="utf-8").strip()

    marker = (
        "<!-- Source: multica-ai/andrej-karpathy-skills; keep in sync with "
        ".codex/skills/karpathy-guidelines/SKILL.md. Claude receives the full version through its plugin. -->"
    )
    section = "## Karpathy Guidelines Condensed"

    assert marker in codex_instructions
    assert section in codex_instructions
    assert codex_instructions.rfind(section) > codex_instructions.rfind("## Subagents")
    assert codex_instructions.endswith("For non-trivial work, define success criteria and run the checks that prove them before claiming completion.")
