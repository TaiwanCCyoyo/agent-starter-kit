import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


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
    antigravity_config = json.loads((ROOT / ".agents" / "hooks.json").read_text(encoding="utf-8"))

    assert set(claude_settings["hooks"]) == {"PostToolUse"}
    assert claude_settings["hooks"]["PostToolUse"][0]["matcher"] == "Edit|Write"
    assert codex_config["hooks"]["PostToolUse"][0]["matcher"] == "apply_patch|Edit|Write"
    assert set(antigravity_config["python-hygiene"]) == {"PostToolUse"}
    assert antigravity_config["python-hygiene"]["PostToolUse"][0]["matcher"] == "edit_file|write_file"
    assert (ROOT / ".claude" / "hooks" / "claude_post_tool_use_hygiene.py").exists()
    assert (ROOT / ".codex" / "hooks" / "codex_post_tool_use_hygiene.py").exists()
    assert (ROOT / ".agents" / "hooks" / "antigravity_post_tool_use_hygiene.py").exists()

    claude_hook = (ROOT / ".claude" / "hooks" / "claude_post_tool_use_hygiene.py").read_text(encoding="utf-8")
    codex_hook = (ROOT / ".codex" / "hooks" / "codex_post_tool_use_hygiene.py").read_text(encoding="utf-8")
    antigravity_hook = (ROOT / ".agents" / "hooks" / "antigravity_post_tool_use_hygiene.py").read_text(encoding="utf-8")
    assert '"E722,F601,F602,F634"' in claude_hook
    assert '"--no-fix"' in claude_hook
    assert '"F401,F841,F842"' in codex_hook
    assert '"--no-fix"' in antigravity_hook
    assert '"F401,F841,F842"' in antigravity_hook


def test_agent_instructions_delegate_pre_commit_owned_checks() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hook_ids = {hook["id"] for repo in config["repos"] for hook in repo["hooks"]}
    instruction_files = [
        ROOT / "AGENTS.md",
        *sorted((ROOT / ".claude" / "rules").rglob("*.md")),
        *sorted((ROOT / ".claude" / "skills").rglob("*.md")),
        *sorted((ROOT / ".codex" / "skills").rglob("*.md")),
        *sorted((ROOT / ".agents" / "skills").rglob("*.md")),
    ]

    assert {"mypy", "ruff", "ruff-format"} <= hook_ids
    for path in instruction_files:
        content = path.read_text(encoding="utf-8").lower()
        assert "uv run ruff" not in content, path
        assert "uv run mypy" not in content, path


def test_hooks_do_not_depend_on_shared_memory_bootstrap() -> None:
    ruff_config = (ROOT / "ruff.toml").read_text(encoding="utf-8")

    assert "[lint.per-file-ignores]" not in ruff_config
    assert "E402" not in ruff_config


def test_codex_uses_native_memories_without_project_mcp_servers() -> None:
    config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))

    assert config["features"]["hooks"] is True
    assert config["features"]["memories"] is True
    assert "mcp_servers" not in config


def test_agent_hook_configs_only_run_read_only_post_tool_diagnostics() -> None:
    codex = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    antigravity = json.loads((ROOT / ".agents" / "hooks.json").read_text(encoding="utf-8"))

    assert set(codex["hooks"]) == {"PostToolUse"}
    assert not (ROOT / ".codex" / "hooks" / "codex_session_start.py").exists()
    assert set(antigravity) == {"python-hygiene"}
    assert set(antigravity["python-hygiene"]) == {"PostToolUse"}
    assert not (ROOT / ".agents" / "workflows").exists()


def test_subagents_handoff_sandbox_failures_to_the_parent() -> None:
    instructions = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "sandbox or permission failures as execution-boundary handoffs" in instructions
    assert "subagents must stop and return the exact error" in instructions
    assert "must not retry, debug permissions" in instructions
    assert "or seek escalated access" in instructions


def test_commit_workflows_do_not_force_ai_attribution() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    antigravity_skill = (ROOT / ".agents" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")

    assert "Co-authored-by:" not in codex_skill
    assert "Agent: Codex" not in codex_skill
    assert "AI-Model:" not in codex_skill
    assert "Co-authored-by:" not in claude_skill
    assert "contributor-model" not in claude_skill
    assert "Co-authored-by:" not in antigravity_skill
    assert "AI-Model:" not in antigravity_skill
    assert "contributor-model" not in antigravity_skill


def test_commit_workflows_do_not_require_agent_status() -> None:
    commit_files = (
        ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md",
        ROOT / ".claude" / "commands" / "gen-commit.md",
        ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md",
        ROOT / ".agents" / "skills" / "gen-commit" / "SKILL.md",
    )

    for path in commit_files:
        assert "Agent-Status" not in path.read_text(encoding="utf-8")


def test_codex_attribution_does_not_require_claude_attribution() -> None:
    codex_skill = (ROOT / ".codex" / "skills" / "gen-commit" / "SKILL.md").read_text(encoding="utf-8")
    claude_skill = (ROOT / ".claude" / "skills" / "commit-helper" / "SKILL.md").read_text(encoding="utf-8")
    claude_command = (ROOT / ".claude" / "commands" / "gen-commit.md").read_text(encoding="utf-8")

    assert "Co-authored-by:" not in codex_skill
    assert "AI-Model:" not in codex_skill

    for content in (claude_skill, claude_command):
        assert "Co-authored-by:" not in content
        assert "contributor-model" not in content

    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    assert settings["includeCoAuthoredBy"] is False
