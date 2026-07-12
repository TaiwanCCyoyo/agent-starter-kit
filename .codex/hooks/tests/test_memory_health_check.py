import importlib.util
import sqlite3
import tomllib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType

from scripts.memory_store import SCHEMA_SQL

ROOT = Path(__file__).parents[3]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


STOP_HOOKS = {
    "claude": load_module("claude_memory_health_check", ROOT / ".claude" / "hooks" / "memory_health_check.py"),
    "codex": load_module("codex_memory_health_check", ROOT / ".codex" / "hooks" / "memory_health_check.py"),
}
CODEX_STOP_HOOK = STOP_HOOKS["codex"]
CLAUDE_STOP_HOOK = STOP_HOOKS["claude"]
CODEX_SESSION_START = load_module("codex_session_start", ROOT / ".codex" / "hooks" / "session_start.py")
CLAUDE_SESSION_START = load_module("claude_session_start", ROOT / ".claude" / "hooks" / "session_start.py")


class HookContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.memory_root = self.root / ".memories"
        self.memory_dir = self.memory_root / "memories"
        self.memory_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def populate_approved(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("Project memory\n", encoding="utf-8")
        (self.memory_dir / "USER.md").write_text("User preference\n", encoding="utf-8")
        (self.memory_root / "memory_store.db").touch()

    def test_approved_layout_produces_no_warning(self) -> None:
        self.populate_approved()
        self.assertEqual(CODEX_STOP_HOOK.memory_taxonomy_message(self.root), "")

    def test_legacy_and_unknown_items_are_flagged(self) -> None:
        for directory in ("changes", "archive", "unknown-repo"):
            with self.subTest(directory=directory):
                self.populate_approved()
                path = self.memory_root / directory
                path.mkdir(exist_ok=True)
                if directory == "unknown-repo":
                    (path / ".git").mkdir()
                self.assertIn(directory + "/", CODEX_STOP_HOOK.memory_taxonomy_message(self.root))
                path.rmdir() if not any(path.iterdir()) else (path / ".git").rmdir()
                if path.exists():
                    path.rmdir()
        legacy = self.memory_dir / "lessons.md"
        legacy.write_text("legacy", encoding="utf-8")
        self.assertIn(
            "memories/lessons.md",
            CODEX_STOP_HOOK.memory_taxonomy_message(self.root),
        )

    def test_memory_character_boundary(self) -> None:
        limit = CODEX_STOP_HOOK.MEMORY_CHAR_LIMIT
        memory = self.memory_dir / "MEMORY.md"
        memory.write_text("x" * limit, encoding="utf-8")
        self.assertEqual(CODEX_STOP_HOOK.memory_health_message(self.root, {}), "")
        memory.write_text("x" * (limit + 1), encoding="utf-8")
        result = CODEX_STOP_HOOK.memory_health_message(self.root, {})
        self.assertIn("getting large", result)
        self.assertIn(str(limit), result)

    def test_user_character_boundary(self) -> None:
        limit = CODEX_STOP_HOOK.USER_CHAR_LIMIT
        user = self.memory_dir / "USER.md"
        user.write_text("x" * limit, encoding="utf-8")
        self.assertEqual(CODEX_STOP_HOOK.user_health_message(self.root), "")
        user.write_text("x" * (limit + 1), encoding="utf-8")
        result = CODEX_STOP_HOOK.user_health_message(self.root)
        self.assertIn("USER.md size reminder", result)
        self.assertIn(str(limit), result)

    def test_missing_memory_and_user_behavior(self) -> None:
        self.assertIn("No MEMORY.md", CODEX_STOP_HOOK.memory_health_message(self.root, {}))
        self.assertEqual(CODEX_STOP_HOOK.user_health_message(self.root), "")

    def test_state_resets_between_sessions(self) -> None:
        CODEX_STOP_HOOK.write_state(self.root, {"session_id": "old", "health_memory_mtime": 9})
        self.assertEqual(CODEX_STOP_HOOK.read_state(self.root, "old")["health_memory_mtime"], 9)
        self.assertEqual(CODEX_STOP_HOOK.read_state(self.root, "new"), {"session_id": "new"})

    def test_stop_hook_has_no_response_count_reminder(self) -> None:
        self.assertFalse(hasattr(CODEX_STOP_HOOK, "memory_update_message"))
        self.assertFalse(hasattr(CODEX_STOP_HOOK, "skill_review_message"))

    def test_taxonomy_warning_keeps_plans_outside_memory(self) -> None:
        self.populate_approved()
        (self.memory_root / "changes").mkdir()
        message = CODEX_STOP_HOOK.memory_taxonomy_message(self.root)
        self.assertIn("Keep planning outside memory", message)
        self.assertIn("project-owned OpenSpec files when initialized", message)


class CodexSessionStartTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_initializes_only_approved_taxonomy(self) -> None:
        result = CODEX_SESSION_START.initialize_memory_taxonomy(self.root, "feat/test")
        memory_root = self.root / ".memories"
        memory_dir = memory_root / "memories"
        self.assertIn("MEMORY.md", result)
        self.assertEqual({path.name for path in memory_dir.iterdir()}, {"MEMORY.md", "USER.md"})
        self.assertTrue((memory_root / "memory_store.db").exists())
        content = (memory_dir / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("feat/test", content)
        self.assertNotIn("# ", content)
        self.assertNotIn("Definition of Done", content)

    def test_user_context_can_be_read_for_injection(self) -> None:
        memory_dir = self.root / ".memories" / "memories"
        memory_dir.mkdir(parents=True)
        (memory_dir / "USER.md").write_text("# User\nTraditional Chinese", encoding="utf-8")
        result = CODEX_SESSION_START.read_text(memory_dir / "USER.md")
        self.assertIn("Traditional Chinese", result)


class ClaudeHookContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.memory_root = self.root / ".memories"
        self.memory_dir = self.memory_root / "memories"
        self.memory_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def populate_approved(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("Project memory\n", encoding="utf-8")
        (self.memory_dir / "USER.md").write_text("User preference\n", encoding="utf-8")
        (self.memory_root / "memory_store.db").touch()

    def test_approved_layout_produces_no_warning(self) -> None:
        self.populate_approved()
        self.assertEqual(CLAUDE_STOP_HOOK.memory_taxonomy_message(self.root), "")

    def test_legacy_and_unknown_items_are_flagged(self) -> None:
        for directory in ("changes", "archive", "unknown-repo"):
            with self.subTest(directory=directory):
                self.populate_approved()
                path = self.memory_root / directory
                path.mkdir(exist_ok=True)
                if directory == "unknown-repo":
                    (path / ".git").mkdir()
                self.assertIn(directory + "/", CLAUDE_STOP_HOOK.memory_taxonomy_message(self.root))
                path.rmdir() if not any(path.iterdir()) else (path / ".git").rmdir()
                if path.exists():
                    path.rmdir()
        legacy = self.memory_dir / "lessons.md"
        legacy.write_text("legacy", encoding="utf-8")
        self.assertIn(
            "memories/lessons.md",
            CLAUDE_STOP_HOOK.memory_taxonomy_message(self.root),
        )

    def test_memory_character_boundary(self) -> None:
        limit = CLAUDE_STOP_HOOK.MEMORY_CHAR_LIMIT
        memory = self.memory_dir / "MEMORY.md"
        memory.write_text("x" * limit, encoding="utf-8")
        self.assertEqual(CLAUDE_STOP_HOOK.memory_health_message(self.root, {}), "")
        memory.write_text("x" * (limit + 1), encoding="utf-8")
        result = CLAUDE_STOP_HOOK.memory_health_message(self.root, {})
        self.assertIn("getting large", result)
        self.assertIn(str(limit), result)

    def test_user_character_boundary(self) -> None:
        limit = CLAUDE_STOP_HOOK.USER_CHAR_LIMIT
        user = self.memory_dir / "USER.md"
        user.write_text("x" * limit, encoding="utf-8")
        self.assertEqual(CLAUDE_STOP_HOOK.user_health_message(self.root), "")
        user.write_text("x" * (limit + 1), encoding="utf-8")
        result = CLAUDE_STOP_HOOK.user_health_message(self.root)
        self.assertIn("USER.md size reminder", result)
        self.assertIn(str(limit), result)

    def test_missing_memory_and_user_behavior(self) -> None:
        self.assertIn("No MEMORY.md", CLAUDE_STOP_HOOK.memory_health_message(self.root, {}))
        self.assertEqual(CLAUDE_STOP_HOOK.user_health_message(self.root), "")

    def test_state_resets_between_sessions(self) -> None:
        CLAUDE_STOP_HOOK.write_state(self.root, {"session_id": "old", "health_memory_mtime": 9})
        self.assertEqual(CLAUDE_STOP_HOOK.read_state(self.root, "old")["health_memory_mtime"], 9)
        self.assertEqual(CLAUDE_STOP_HOOK.read_state(self.root, "new"), {"session_id": "new"})

    def test_stop_hook_has_no_response_count_reminder(self) -> None:
        self.assertFalse(hasattr(CLAUDE_STOP_HOOK, "memory_update_message"))
        self.assertFalse(hasattr(CLAUDE_STOP_HOOK, "skill_review_message"))

    def test_taxonomy_warning_keeps_plans_outside_memory(self) -> None:
        self.populate_approved()
        (self.memory_root / "changes").mkdir()
        message = CLAUDE_STOP_HOOK.memory_taxonomy_message(self.root)
        self.assertIn("Keep planning outside memory", message)
        self.assertIn("project-owned OpenSpec files when initialized", message)


class ClaudeSessionStartTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_initializes_only_approved_taxonomy(self) -> None:
        result = CLAUDE_SESSION_START.initialize_memory_taxonomy(self.root, "feat/test")
        memory_root = self.root / ".memories"
        memory_dir = memory_root / "memories"
        self.assertIn("MEMORY.md", result)
        self.assertEqual({path.name for path in memory_dir.iterdir()}, {"MEMORY.md", "USER.md"})
        self.assertTrue((memory_root / "memory_store.db").exists())
        content = (memory_dir / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("feat/test", content)
        self.assertNotIn("# ", content)
        self.assertNotIn("Definition of Done", content)

    def test_user_context_can_be_read_for_injection(self) -> None:
        memory_dir = self.root / ".memories" / "memories"
        memory_dir.mkdir(parents=True)
        (memory_dir / "USER.md").write_text("# User\nTraditional Chinese", encoding="utf-8")
        result = CLAUDE_SESSION_START.read_text(memory_dir / "USER.md")
        self.assertIn("Traditional Chinese", result)


class ClaudeMCPConfigTests(unittest.TestCase):
    def test_claude_hooks_use_exec_form_with_project_dir_placeholder(self) -> None:
        import json

        config = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        for event in ("SessionStart", "PostToolUse", "Stop"):
            hook = config["hooks"][event][0]["hooks"][0]
            self.assertEqual(hook["command"], "uv")
            self.assertTrue(any("${CLAUDE_PROJECT_DIR}" in arg for arg in hook["args"]))

    def test_memory_store_is_project_scoped(self) -> None:
        import json

        config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["memory-db"]
        self.assertEqual(server["command"], "uvx")
        self.assertIn(".memories/memory_store.db", server["args"][-1])

    def test_claude_targets_holographic_compatible_store(self) -> None:
        import json

        config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        args = config["mcpServers"]["memory-db"]["args"]
        self.assertIn("memory_store.db", args[-1])

    def test_memory_control_server_is_not_registered(self) -> None:
        import json

        config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        self.assertNotIn("memory-control", config["mcpServers"])


class CodexMCPConfigTests(unittest.TestCase):
    def test_memory_control_server_is_not_registered(self) -> None:
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        self.assertNotIn("memory-control", config["mcp_servers"])

    def test_memory_store_is_project_scoped(self) -> None:
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        server = config["mcp_servers"]["memory-db"]
        self.assertEqual(server["command"], "uvx")
        self.assertEqual(
            server["args"],
            ["mcp-server-sqlite", "--db-path", ".memories/memory_store.db"],
        )
        self.assertEqual(server["cwd"], "..")
        self.assertFalse(server["required"])
        self.assertEqual(server["default_tools_approval_mode"], "prompt")
        self.assertEqual(server["tools"]["read_query"]["approval_mode"], "auto")
        self.assertEqual(server["tools"]["list_tables"]["approval_mode"], "auto")
        self.assertEqual(server["tools"]["describe_table"]["approval_mode"], "auto")

    def test_codex_targets_holographic_compatible_store(self) -> None:
        codex = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        codex_args = codex["mcp_servers"]["memory-db"]["args"]
        self.assertEqual(codex_args[-1], ".memories/memory_store.db")


class FTS5TriggerTests(unittest.TestCase):
    def make_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_SQL)
        return conn

    def insert_entry(self, conn: sqlite3.Connection, content: str, tags: str) -> None:
        conn.execute(
            "INSERT INTO facts (content, category, tags) VALUES (?, ?, ?)",
            (content, "lesson", tags),
        )
        conn.commit()

    def test_insert_update_delete_keep_index_in_sync(self) -> None:
        conn = self.make_db()
        self.insert_entry(conn, "old body content", "old-tag")
        self.assertEqual(len(conn.execute("SELECT rowid FROM facts_fts WHERE facts_fts MATCH 'old'").fetchall()), 1)
        conn.execute("UPDATE facts SET content = 'new body', tags = 'new-tag' WHERE content = 'old body content'")
        conn.commit()
        self.assertEqual(len(conn.execute("SELECT rowid FROM facts_fts WHERE facts_fts MATCH 'old'").fetchall()), 0)
        self.assertEqual(len(conn.execute("SELECT rowid FROM facts_fts WHERE facts_fts MATCH 'new'").fetchall()), 1)
        conn.execute("DELETE FROM facts WHERE content = 'new body'")
        conn.commit()
        self.assertEqual(len(conn.execute("SELECT rowid FROM facts_fts WHERE facts_fts MATCH 'new'").fetchall()), 0)

    def test_problem_occurrences_support_repeat_detection(self) -> None:
        conn = self.make_db()
        conn.execute(
            "INSERT INTO problem_patterns (fingerprint, title, symptoms, status) VALUES (?, ?, ?, ?)",
            ("same-error", "Repeated error", "same symptom", "observed"),
        )
        pattern_id = conn.execute("SELECT pattern_id FROM problem_patterns").fetchone()[0]
        conn.executemany(
            "INSERT INTO problem_occurrences (pattern_id, evidence) VALUES (?, ?)",
            [(pattern_id, "first"), (pattern_id, "second")],
        )
        conn.commit()
        count = conn.execute("SELECT occurrence_count FROM problem_patterns").fetchone()[0]
        self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
