import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SESSION_HOOKS = (
    ROOT / ".agent" / "hooks" / "session_start.py",
    ROOT / ".codex" / "hooks" / "session_start.py",
)


def test_pre_commit_mypy_receives_targeted_python_files() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    local_repo = next(repo for repo in config["repos"] if repo["repo"] == "local")
    mypy_hook = next(hook for hook in local_repo["hooks"] if hook["id"] == "mypy")

    assert mypy_hook["entry"] == "uv run mypy --explicit-package-bases"
    assert mypy_hook.get("pass_filenames", True) is True
    assert mypy_hook["types"] == ["python"]


def test_claude_uses_pyright_lsp_without_project_ruff_lsp() -> None:
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))

    assert settings["enabledPlugins"]["pyright-lsp@claude-plugins-official"] is True
    assert "ruff-lsp@agent-starter-kit" not in settings["enabledPlugins"]
    assert "agent-starter-kit" not in settings["extraKnownMarketplaces"]
    assert not (ROOT / ".claude" / "marketplace").exists()


def test_claude_native_workflow_does_not_require_external_workflow_plugins() -> None:
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    plugins = settings["enabledPlugins"]

    assert plugins["superpowers@claude-plugins-official"] is False
    assert plugins["ponytail@ponytail"] is False
    assert plugins["andrej-karpathy-skills@karpathy-skills"] is False
    assert plugins["github@claude-plugins-official"] is True
    assert plugins["skill-creator@claude-plugins-official"] is True
    assert not (ROOT / ".codex" / "skills" / "karpathy-guidelines").exists()


def test_claude_and_codex_use_read_only_ruff_diagnostics() -> None:
    claude_settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    codex_config = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    antigravity_config = json.loads((ROOT / ".agent" / "hooks.json").read_text(encoding="utf-8"))

    assert set(claude_settings["hooks"]) == {"PostToolUse"}
    assert claude_settings["hooks"]["PostToolUse"][0]["matcher"] == "Edit|Write"
    assert codex_config["hooks"]["PostToolUse"][0]["matcher"] == "apply_patch|Edit|Write"
    assert antigravity_config["hooks"]["PostToolUse"][0]["matcher"] == "*"
    assert (ROOT / ".claude" / "hooks" / "post_tool_use_hygiene.py").exists()
    assert (ROOT / ".codex" / "hooks" / "post_tool_use_hygiene.py").exists()
    assert (ROOT / ".agent" / "hooks" / "post_tool_use_hygiene.py").exists()

    claude_hook = (ROOT / ".claude" / "hooks" / "post_tool_use_hygiene.py").read_text(encoding="utf-8")
    codex_hook = (ROOT / ".codex" / "hooks" / "post_tool_use_hygiene.py").read_text(encoding="utf-8")
    antigravity_hook = (ROOT / ".agent" / "hooks" / "post_tool_use_hygiene.py").read_text(encoding="utf-8")
    assert '"E722,F601,F602,F634"' in claude_hook
    assert '"--no-fix"' in claude_hook
    assert '"F401,F841,F842"' in codex_hook
    assert '"E722,F601,F602,F634"' in antigravity_hook
    assert '"--no-fix"' in antigravity_hook


def test_agent_instructions_delegate_pre_commit_owned_checks() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hook_ids = {hook["id"] for repo in config["repos"] for hook in repo["hooks"]}
    instruction_files = [
        ROOT / "CLAUDE.md",
        ROOT / "GEMINI.md",
        ROOT / ".codex" / "AGENTS.md",
        *sorted((ROOT / ".agent" / "workflows").rglob("*.md")),
        *sorted((ROOT / ".agent" / "skills").rglob("*.md")),
        *sorted((ROOT / ".claude" / "rules").rglob("*.md")),
        *sorted((ROOT / ".claude" / "skills").rglob("*.md")),
        *sorted((ROOT / ".codex" / "skills").rglob("*.md")),
    ]

    assert {"mypy", "ruff", "ruff-format"} <= hook_ids
    for path in instruction_files:
        content = path.read_text(encoding="utf-8").lower()
        assert "uv run ruff" not in content, path
        assert "uv run mypy" not in content, path


def test_session_hooks_do_not_depend_on_shared_memory_bootstrap() -> None:
    ruff_config = (ROOT / "ruff.toml").read_text(encoding="utf-8")

    assert "[lint.per-file-ignores]" not in ruff_config
    assert "E402" not in ruff_config

    for hook_path in SESSION_HOOKS:
        hook_content = hook_path.read_text(encoding="utf-8")
        assert "def main(" in hook_content


def test_codex_uses_native_memories_without_project_mcp_servers() -> None:
    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))

    assert config["features"]["hooks"] is True
    assert config["features"]["memories"] is True
    assert "mcp_servers" not in config


def test_agent_hook_configs_have_no_stop_event() -> None:
    codex = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    antigravity = json.loads((ROOT / ".agent" / "hooks.json").read_text(encoding="utf-8"))

    assert set(codex["hooks"]) == {"SessionStart", "PostToolUse"}
    assert set(antigravity["hooks"]) == {"SessionStart", "PostToolUse"}


def test_claude_instructions_use_direct_openspec_routing() -> None:
    claude_instructions = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert ("downstream" + " project") not in claude_instructions.lower()
    assert "OpenSpec" in claude_instructions


def test_root_agent_instructions_remain_bounded_routing_maps() -> None:
    instructions = {
        ROOT / "CLAUDE.md": 80,
        ROOT / "GEMINI.md": 90,
        ROOT / ".codex" / "AGENTS.md": 90,
    }

    for path, max_lines in instructions.items():
        content = path.read_text(encoding="utf-8")
        assert len(content.splitlines()) <= max_lines
        assert "## Karpathy Guidelines Condensed" not in content


def test_codex_subagents_handoff_sandbox_failures_to_the_parent() -> None:
    instructions = (ROOT / ".codex" / "AGENTS.md").read_text(encoding="utf-8")

    assert "sandbox or permission failures as execution-boundary handoffs" in instructions
    assert "subagents must stop and return the exact error" in instructions
    assert "must not retry, debug permissions" in instructions
    assert "or seek escalated access" in instructions


def test_codex_agents_keep_unique_roles_and_bounded_permissions() -> None:
    agent_dir = ROOT / ".codex" / "agents"

    assert {path.stem for path in agent_dir.glob("*.toml")} == {
        "commit-specialist",
        "doc-translator",
        "signal-miner",
        "implementation-reviewer",
        "plan-reviewer",
        "security-reviewer",
        "task-worker",
    }

    names: set[str] = set()
    writable = {"task_worker", "commit-specialist", "doc_translator"}
    for path in agent_dir.glob("*.toml"):
        config = tomllib.loads(path.read_text(encoding="utf-8"))
        assert config["name"] not in names
        names.add(config["name"])
        assert config["model"]
        assert config["model_reasoning_effort"] in {"low", "medium", "high", "xhigh", "max", "ultra"}
        assert config["sandbox_mode"] == ("workspace-write" if config["name"] in writable else "read-only")

    task_worker = tomllib.loads((agent_dir / "task-worker.toml").read_text(encoding="utf-8"))
    assert task_worker["sandbox_mode"] == "workspace-write"
    assert "bounded" in task_worker["description"].lower()
    assert "planning" in task_worker["description"].lower()

    signal_miner = tomllib.loads((agent_dir / "signal-miner.toml").read_text(encoding="utf-8"))
    assert signal_miner["sandbox_mode"] == "read-only"
    assert "low-cost" in signal_miner["description"].lower()
    assert "verbose" in signal_miner["description"].lower()


def test_claude_agent_model_routing_uses_current_aliases() -> None:
    expected = {
        "commit-specialist": ("haiku", None),
        "doc-translator": ("haiku", None),
        "signal-miner": ("haiku", None),
        "implementation-reviewer": ("opus", "high"),
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


def test_task_worker_descriptions_do_not_upgrade_low_cost_sessions() -> None:
    instructions = (
        (ROOT / ".codex" / "agents" / "task-worker.toml").read_text(encoding="utf-8"),
        (ROOT / ".claude" / "agents" / "task-worker.md").read_text(encoding="utf-8"),
    )

    for content in instructions:
        lowered = content.lower()
        assert "lowest-cost" in lowered
        assert "do not use" in lowered
        assert "raise capability" not in lowered
        assert "capability floor" not in lowered


def test_signal_miner_descriptions_route_high_output_commands() -> None:
    """The description must still name the high-output command families it owns.

    Wording is intentionally not frozen; only the routing signal is asserted.
    """
    claude_frontmatter = (ROOT / ".claude" / "agents" / "signal-miner.md").read_text(encoding="utf-8").split("---", 2)[1].lower()
    codex_config = tomllib.loads((ROOT / ".codex" / "agents" / "signal-miner.toml").read_text(encoding="utf-8"))

    for description in (claude_frontmatter, codex_config["description"].lower()):
        for command_family in ("verbose diagnostics", "dependency traces"):
            assert command_family in description
        assert "read-only" in description
        assert "explore" in description


def test_low_tier_agent_handoffs_are_bounded_and_explicit() -> None:
    codex_agents = (
        (ROOT / ".codex" / "agents" / "commit-specialist.toml").read_text(encoding="utf-8"),
        (ROOT / ".codex" / "agents" / "signal-miner.toml").read_text(encoding="utf-8"),
        (ROOT / ".codex" / "agents" / "doc-translator.toml").read_text(encoding="utf-8"),
    )
    claude_agents = (
        (ROOT / ".claude" / "agents" / "commit-specialist.md").read_text(encoding="utf-8"),
        (ROOT / ".claude" / "agents" / "signal-miner.md").read_text(encoding="utf-8"),
        (ROOT / ".claude" / "agents" / "doc-translator.md").read_text(encoding="utf-8"),
    )
    commit_workflows = (
        (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8"),
        (ROOT / ".claude" / "commands" / "gen-commit.md").read_text(encoding="utf-8"),
        (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8"),
    )

    for content in (*codex_agents, *claude_agents):
        assert "one concrete objective" in content
        assert "acceptance criteria" in content
        assert "parent agent" in content
        assert "stop" in content.lower()

    for content in commit_workflows:
        assert "submodule" in content
        assert "git add -- <submodule-path>" in content
        assert "must not commit inside a submodule" in content

    for content in (codex_agents[2], claude_agents[2]):
        assert "explicit target" in content
        assert "source diff" in content


def test_commit_workflows_do_not_force_ai_attribution() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    codex_agent = (ROOT / ".codex" / "agents" / "commit-specialist.toml").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    claude_agent = (ROOT / ".claude" / "agents" / "commit-specialist.md").read_text(encoding="utf-8")

    for content in (codex_skill, codex_agent):
        assert "Co-authored-by:" not in content
        assert "Agent: Codex" not in content

    assert "AI-Model:" not in codex_skill
    assert "AI-Model:" not in codex_agent

    for content in (claude_skill, claude_agent):
        assert "Co-authored-by:" not in content
        assert "contributor-model" not in content

    assert "  - Edit" in claude_agent
    assert "Follow `.claude/skills/commit-helper/SKILL.md` as the source of truth." in claude_agent


def test_commit_workflows_do_not_require_agent_status() -> None:
    commit_files = (
        ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md",
        ROOT / ".codex" / "agents" / "commit-specialist.toml",
        ROOT / ".claude" / "commands" / "gen-commit.md",
        ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md",
        ROOT / ".claude" / "agents" / "commit-specialist.md",
        ROOT / ".agent" / "workflows" / "gen-commit.md",
        ROOT / ".agent" / "skills" / "commit-helper" / "SKILL.md",
    )

    for path in commit_files:
        assert "Agent-Status" not in path.read_text(encoding="utf-8")


def test_codex_attribution_does_not_require_claude_attribution() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    codex_agent = (ROOT / ".codex" / "agents" / "commit-specialist.toml").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    claude_command = (ROOT / ".claude" / "commands" / "gen-commit.md").read_text(encoding="utf-8")
    claude_agent = (ROOT / ".claude" / "agents" / "commit-specialist.md").read_text(encoding="utf-8")

    assert "Co-authored-by:" not in codex_skill
    assert "Co-authored-by:" not in codex_agent
    assert "AI-Model:" not in codex_skill
    assert "AI-Model:" not in codex_agent

    for content in (claude_skill, claude_command, claude_agent):
        assert "Co-authored-by:" not in content
        assert "contributor-model" not in content

    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    assert settings["includeCoAuthoredBy"] is False


def test_commit_specialists_use_explicit_delegation_modes() -> None:
    codex_files = (
        ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md",
        ROOT / ".codex" / "agents" / "commit-specialist.toml",
    )
    claude_files = (
        ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md",
        ROOT / ".claude" / "commands" / "gen-commit.md",
        ROOT / ".claude" / "agents" / "commit-specialist.md",
    )

    for path in codex_files:
        content = path.read_text(encoding="utf-8").lower()
        assert "accept supplied message" in content
        assert "review supplied message" in content
        assert "complete rough or missing message" in content

    for path in claude_files:
        content = path.read_text(encoding="utf-8").lower()
        assert "execute supplied message" in content
        assert "review supplied message" in content
        assert "complete rough or missing message" in content

    codex_skill = codex_files[0].read_text(encoding="utf-8")
    codex_agent = codex_files[1].read_text(encoding="utf-8")
    assert "Do not automatically escalate to diff review" in codex_skill
    assert "Run pre-commit against the explicitly approved paths" in codex_agent
    assert "execute `git commit` with the approved message" in codex_agent
    assert "Never retry a sandbox-failed step" in codex_agent
    assert "relocate or rebuild caches" in codex_agent
    assert "change ACLs" in codex_agent
    assert "Never promote `accept supplied message`" in codex_agent
    assert "do not inspect content" in codex_agent

    assert "Unknown change intent" in codex_skill
    assert "Approximate change intent" in codex_skill
    assert "Exact intent in a clean, well-understood scope" in codex_skill
    assert "Exact intent but explicit double-check requested" in codex_skill
    assert "must not promote itself into this mode" in codex_skill

    claude_skill = claude_files[0].read_text(encoding="utf-8")
    assert "Do not duplicate diff review" in claude_skill
    assert "delegate it to `commit-specialist`" in claude_skill
    assert "Unknown change intent" in claude_skill
    assert "Approximate change intent" in claude_skill
    assert "Exact intent in a clean, well-understood scope" in claude_skill
    assert "Exact intent but explicit double-check requested" in claude_skill
    assert "must not promote itself into this mode" in claude_skill

    claude_agent = claude_files[2].read_text(encoding="utf-8")
    assert "Never promote **execute supplied message**" in claude_agent
    assert "Run pre-commit against the explicitly approved paths" in claude_agent

    for path in (codex_files[0], claude_files[0], claude_files[2]):
        content = path.read_text(encoding="utf-8")
        assert "simple, directly actionable" in content
        assert "retry once" in content
