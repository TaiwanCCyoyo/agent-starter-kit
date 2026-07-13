import tomllib
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


def test_codex_agent_model_routing_uses_current_tiers() -> None:
    expected = {
        "plan_reviewer": ("gpt-5.6", "high"),
        "implementation_reviewer": ("gpt-5.6", "high"),
        "security_reviewer": ("gpt-5.6", "high"),
        "task_worker": ("gpt-5.6-terra", "medium"),
        "signal_miner": ("gpt-5.6-luna", "medium"),
        "commit_specialist": ("gpt-5.6-luna", "medium"),
        "doc_translator": ("gpt-5.6-terra", "low"),
        "memory_auditor": ("gpt-5.6-luna", "medium"),
        "memory_compressor": ("gpt-5.6-terra", "medium"),
    }
    agent_dir = ROOT / ".codex" / "agents"

    assert {path.stem for path in agent_dir.glob("*.toml")} == {
        "commit-specialist",
        "doc-translator",
        "signal-miner",
        "implementation-reviewer",
        "memory-auditor",
        "memory-compressor",
        "plan-reviewer",
        "security-reviewer",
        "task-worker",
    }

    for path in agent_dir.glob("*.toml"):
        config = tomllib.loads(path.read_text(encoding="utf-8"))
        model, effort = expected[config["name"]]
        assert config["model"] == model
        assert config["model_reasoning_effort"] == effort

    task_worker = tomllib.loads((agent_dir / "task-worker.toml").read_text(encoding="utf-8"))
    assert task_worker["sandbox_mode"] == "workspace-write"
    assert "bounded" in task_worker["description"].lower()
    assert "planning" in task_worker["description"].lower()

    signal_miner = tomllib.loads((agent_dir / "signal-miner.toml").read_text(encoding="utf-8"))
    assert signal_miner["sandbox_mode"] == "read-only"
    assert "lowest-cost" in signal_miner["description"].lower()
    assert "verbose" in signal_miner["description"].lower()


def test_claude_agent_model_routing_uses_current_aliases() -> None:
    expected = {
        "commit-specialist": ("haiku", None),
        "doc-translator": ("sonnet", "low"),
        "signal-miner": ("haiku", None),
        "implementation-reviewer": ("opus", "high"),
        "memory-auditor": ("haiku", None),
        "memory-compressor": ("sonnet", "medium"),
        "plan-reviewer": ("opus", "high"),
        "security-reviewer": ("opus", "high"),
        "task-worker": ("sonnet", "medium"),
    }
    agent_dir = ROOT / ".claude" / "agents"

    assert {path.stem for path in agent_dir.glob("*.md")} == set(expected)

    for path in agent_dir.glob("*.md"):
        frontmatter = path.read_text(encoding="utf-8").split("---", 2)[1]
        fields = dict(line.split(":", 1) for line in frontmatter.splitlines() if ":" in line and not line.startswith((" ", "-")))
        model, effort = expected[path.stem]
        assert fields["model"].strip() == model
        if effort is None:
            assert "effort" not in fields
        else:
            assert fields["effort"].strip() == effort

    task_worker = (agent_dir / "task-worker.md").read_text(encoding="utf-8")
    assert "bounded" in task_worker.split("---", 2)[1].lower()
    assert "planning" in task_worker.split("---", 2)[1].lower()
    assert "  - Write" in task_worker
    assert "  - Edit" in task_worker

    signal_miner = (agent_dir / "signal-miner.md").read_text(encoding="utf-8")
    assert "lowest-cost" in signal_miner.split("---", 2)[1].lower()
    assert "verbose" in signal_miner.split("---", 2)[1].lower()
    assert "  - Write" not in signal_miner
    assert "  - Edit" not in signal_miner


def test_main_agent_cost_routing_does_not_upgrade_low_cost_sessions() -> None:
    instructions = (
        (ROOT / ".codex" / "AGENTS.md").read_text(encoding="utf-8"),
        (ROOT / "CLAUDE.md").read_text(encoding="utf-8"),
    )

    for content in instructions:
        lowered = content.lower()
        assert "signal_miner" in content or "signal-miner" in content
        assert "lowest-cost" in lowered
        assert "do not escalate" in lowered
        assert "raise capability" not in lowered
        assert "capability floor" not in lowered


def test_commit_agents_use_formal_coauthor_identity_trailers() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    codex_agent = (ROOT / ".codex" / "agents" / "commit-specialist.toml").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    claude_agent = (ROOT / ".claude" / "agents" / "commit-specialist.md").read_text(encoding="utf-8")

    for content in (codex_skill, codex_agent):
        assert "Co-authored-by: Codex <codex@openai.com>" in content
        assert "Agent: Codex" not in content

    assert "AI-Model: gpt-5.6-luna" not in codex_skill
    assert "main agent selects the ordered list" in codex_skill
    assert "AI-Model: gpt-5.6-luna" not in codex_agent

    for content in (claude_skill, claude_agent):
        assert "Co-authored-by: Claude <resolved model display name> <noreply@anthropic.com>" in content
        assert "Co-authored-by: Claude <noreply@anthropic.com>" in content
        assert "Agent: Claude" not in content

    assert "Do not add an `AI-Model` trailer" in claude_skill
    assert "  - Edit" in claude_agent
    assert "Follow `.claude/skills/commit-helper/SKILL.md` as the source of truth." in claude_agent


def test_commit_model_attribution_is_selected_by_the_parent_agent() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    codex_agent = (ROOT / ".codex" / "agents" / "commit-specialist.toml").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    claude_command = (ROOT / ".claude" / "commands" / "gen-commit.md").read_text(encoding="utf-8")
    claude_agent = (ROOT / ".claude" / "agents" / "commit-specialist.md").read_text(encoding="utf-8")

    assert "ordered list of material contributor models" in codex_skill
    assert "request it before drafting or committing" in codex_skill
    assert "AI-Model: gpt-5.6\nAI-Model: gpt-5.6-terra" in codex_skill
    assert "Do not infer, add, reorder, or replace" in codex_agent
    assert "AI-Model: gpt-5.6-luna" not in codex_agent

    for content in (claude_skill, claude_command):
        assert "contributor-model context and roles" in content
    assert "final discretion" not in claude_agent
    assert "final discretion" not in claude_skill
    assert "must request it before drafting or committing" in claude_skill
    assert "Request contributor-model context from the parent" in claude_agent
    assert "do not merge, omit, infer, or substitute contributors" in claude_agent
    assert "Do not add an `AI-Model` trailer" in claude_skill
