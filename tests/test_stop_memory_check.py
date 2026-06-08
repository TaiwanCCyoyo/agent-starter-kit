import importlib.util
import sqlite3
import tomllib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType

ROOT = Path(__file__).parent.parent


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


STOP_HOOKS = {
    "claude": load_module("claude_stop_memory_check", ROOT / ".claude" / "hooks" / "stop_memory_check.py"),
    "codex": load_module("codex_stop_memory_check", ROOT / ".codex" / "hooks" / "stop_memory_check.py"),
}
CODEX_SESSION_START = load_module("codex_session_start", ROOT / ".codex" / "hooks" / "session_start.py")


class HookContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.memory_dir = self.root / ".agents" / "memory"
        self.memory_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def populate_approved(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("# Memory\n", encoding="utf-8")
        (self.memory_dir / "USER.md").write_text("# User\n", encoding="utf-8")
        (self.memory_dir / "decisions.md").write_text("", encoding="utf-8")
        (self.memory_dir / "lessons.md").write_text("", encoding="utf-8")
        (self.memory_dir / "changes").mkdir(exist_ok=True)
        (self.memory_dir / "archive").mkdir(exist_ok=True)

    def test_approved_layout_produces_no_warning(self) -> None:
        self.populate_approved()
        for name, hook in STOP_HOOKS.items():
            with self.subTest(hook=name):
                self.assertEqual(hook.memory_taxonomy_message(self.root), "")

    def test_legacy_and_unknown_directories_are_flagged(self) -> None:
        for directory in ("runs", "candidates", "unknown-repo"):
            with self.subTest(directory=directory):
                self.populate_approved()
                path = self.memory_dir / directory
                path.mkdir(exist_ok=True)
                if directory == "unknown-repo":
                    (path / ".git").mkdir()
                for name, hook in STOP_HOOKS.items():
                    with self.subTest(hook=name):
                        self.assertIn(directory + "/", hook.memory_taxonomy_message(self.root))
                path.rmdir() if not any(path.iterdir()) else (path / ".git").rmdir()
                if path.exists():
                    path.rmdir()

    def test_memory_character_boundary(self) -> None:
        for name, hook in STOP_HOOKS.items():
            with self.subTest(hook=name):
                limit = hook.MEMORY_CHAR_LIMIT
                memory = self.memory_dir / "MEMORY.md"
                memory.write_text("x" * limit, encoding="utf-8")
                self.assertEqual(hook.memory_health_message(self.root, {}), "")
                memory.write_text("x" * (limit + 1), encoding="utf-8")
                result = hook.memory_health_message(self.root, {})
                self.assertIn("getting large", result)
                self.assertIn(str(limit), result)

    def test_user_character_boundary(self) -> None:
        for name, hook in STOP_HOOKS.items():
            with self.subTest(hook=name):
                limit = hook.USER_CHAR_LIMIT
                user = self.memory_dir / "USER.md"
                user.write_text("x" * limit, encoding="utf-8")
                self.assertEqual(hook.user_health_message(self.root), "")
                user.write_text("x" * (limit + 1), encoding="utf-8")
                result = hook.user_health_message(self.root)
                self.assertIn("USER.md size reminder", result)
                self.assertIn(str(limit), result)

    def test_missing_memory_and_user_behavior(self) -> None:
        for name, hook in STOP_HOOKS.items():
            with self.subTest(hook=name):
                self.assertIn("No MEMORY.md", hook.memory_health_message(self.root, {}))
                self.assertEqual(hook.user_health_message(self.root), "")

    def test_state_resets_between_sessions(self) -> None:
        for name, hook in STOP_HOOKS.items():
            with self.subTest(hook=name):
                hook.write_state(self.root, {"session_id": "old", "response_count": 9})
                self.assertEqual(hook.read_state(self.root, "old")["response_count"], 9)
                self.assertEqual(hook.read_state(self.root, "new"), {"session_id": "new"})


class CodexSessionStartTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_initializes_only_approved_taxonomy(self) -> None:
        result = CODEX_SESSION_START.initialize_memory_taxonomy(self.root, "feat/test")
        memory_dir = self.root / ".agents" / "memory"
        self.assertIn("MEMORY.md", result)
        self.assertEqual(
            {path.name for path in memory_dir.iterdir()},
            {"MEMORY.md", "USER.md", "decisions.md", "lessons.md", "changes", "archive"},
        )
        self.assertIn("feat/test", (memory_dir / "MEMORY.md").read_text(encoding="utf-8"))

    def test_user_context_can_be_read_for_injection(self) -> None:
        memory_dir = self.root / ".agents" / "memory"
        memory_dir.mkdir(parents=True)
        (memory_dir / "USER.md").write_text("# User\nTraditional Chinese", encoding="utf-8")
        result = CODEX_SESSION_START.read_text(memory_dir / "USER.md")
        self.assertIn("Traditional Chinese", result)


class CodexMCPConfigTests(unittest.TestCase):
    def test_memory_db_is_project_scoped_and_shared(self) -> None:
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        server = config["mcp_servers"]["memory-db"]
        self.assertEqual(server["command"], "uvx")
        self.assertEqual(
            server["args"],
            ["mcp-server-sqlite", "--db-path", ".agents/memory/memory.db"],
        )
        self.assertEqual(server["cwd"], "..")
        self.assertFalse(server["required"])
        self.assertEqual(server["default_tools_approval_mode"], "prompt")
        self.assertEqual(server["tools"]["read_query"]["approval_mode"], "auto")
        self.assertEqual(server["tools"]["list_tables"]["approval_mode"], "auto")
        self.assertEqual(server["tools"]["describe_table"]["approval_mode"], "auto")

    def test_codex_and_claude_target_same_database(self) -> None:
        codex = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        codex_args = codex["mcp_servers"]["memory-db"]["args"]
        claude_text = (ROOT / ".mcp.json").read_text(encoding="utf-8")
        self.assertEqual(codex_args[-1], ".agents/memory/memory.db")
        self.assertIn(".agents/memory/memory.db", claude_text)


class FTS5TriggerTests(unittest.TestCase):
    def make_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(":memory:")
        conn.executescript(
            """
            CREATE TABLE memory_entries (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                cwd TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                type TEXT NOT NULL CHECK(type IN ('lesson','decision','workflow','run-note','candidate')),
                tags TEXT,
                summary TEXT NOT NULL,
                body TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE memory_fts USING fts5(
                summary,
                body,
                content='memory_entries',
                content_rowid='id'
            );
            CREATE TRIGGER memory_ai AFTER INSERT ON memory_entries BEGIN
                INSERT INTO memory_fts(rowid, summary, body)
                VALUES (new.id, new.summary, new.body);
            END;
            CREATE TRIGGER memory_ad AFTER DELETE ON memory_entries BEGIN
                INSERT INTO memory_fts(memory_fts, rowid, summary, body)
                VALUES ('delete', old.id, old.summary, old.body);
            END;
            CREATE TRIGGER memory_au AFTER UPDATE ON memory_entries BEGIN
                INSERT INTO memory_fts(memory_fts, rowid, summary, body)
                VALUES ('delete', old.id, old.summary, old.body);
                INSERT INTO memory_fts(rowid, summary, body)
                VALUES (new.id, new.summary, new.body);
            END;
            CREATE TABLE sessions (
                session_id TEXT PRIMARY KEY,
                cwd TEXT NOT NULL,
                started_at TEXT NOT NULL DEFAULT (datetime('now')),
                stopped_at TEXT
            );
            """
        )
        return conn

    def insert_entry(self, conn: sqlite3.Connection, summary: str, body: str) -> None:
        conn.execute(
            "INSERT INTO memory_entries (session_id, cwd, type, summary, body) VALUES (?, ?, ?, ?, ?)",
            ("session-1", "C:/repo", "lesson", summary, body),
        )
        conn.commit()

    def test_insert_update_delete_keep_index_in_sync(self) -> None:
        conn = self.make_db()
        self.insert_entry(conn, "old summary", "old body content")
        self.assertEqual(len(conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'old'").fetchall()), 1)
        conn.execute("UPDATE memory_entries SET summary = 'new summary', body = 'new body' WHERE summary = 'old summary'")
        conn.commit()
        self.assertEqual(len(conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'old'").fetchall()), 0)
        self.assertEqual(len(conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'new'").fetchall()), 1)
        conn.execute("DELETE FROM memory_entries WHERE summary = 'new summary'")
        conn.commit()
        self.assertEqual(len(conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'new'").fetchall()), 0)

    def test_session_upsert_is_idempotent(self) -> None:
        conn = self.make_db()
        statement = "INSERT INTO sessions (session_id, cwd) VALUES (?, ?) ON CONFLICT(session_id) DO NOTHING"
        conn.execute(statement, ("session-1", "C:/repo"))
        conn.execute(statement, ("session-1", "C:/other"))
        conn.commit()
        rows = conn.execute("SELECT session_id, cwd FROM sessions").fetchall()
        self.assertEqual(rows, [("session-1", "C:/repo")])


if __name__ == "__main__":
    unittest.main()
