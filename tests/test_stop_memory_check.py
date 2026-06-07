import importlib.util
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# .claude/ is a dot-prefixed directory, not importable as a package; load via file path.
_HOOK_PATH = Path(__file__).parent.parent / ".claude" / "hooks" / "stop_memory_check.py"
_spec = importlib.util.spec_from_file_location("stop_memory_check", _HOOK_PATH)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

MEMORY_CHAR_LIMIT: int = _mod.MEMORY_CHAR_LIMIT
USER_CHAR_LIMIT: int = _mod.USER_CHAR_LIMIT
memory_health_message = _mod.memory_health_message
memory_taxonomy_message = _mod.memory_taxonomy_message
user_health_message = _mod.user_health_message


class MemoryTaxonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.memory_dir = self.root / ".agents" / "memory"
        self.memory_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def _populate_approved(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("# Memory\n", encoding="utf-8")
        (self.memory_dir / "USER.md").write_text("# User\n", encoding="utf-8")
        (self.memory_dir / "decisions.md").write_text("", encoding="utf-8")
        (self.memory_dir / "lessons.md").write_text("", encoding="utf-8")
        (self.memory_dir / "changes").mkdir(exist_ok=True)
        (self.memory_dir / "archive").mkdir(exist_ok=True)

    def test_approved_layout_produces_no_warning(self) -> None:
        self._populate_approved()
        self.assertEqual(memory_taxonomy_message(self.root), "")

    def test_legacy_runs_dir_produces_warning(self) -> None:
        self._populate_approved()
        (self.memory_dir / "runs").mkdir()
        result = memory_taxonomy_message(self.root)
        self.assertIn("runs/", result)

    def test_unknown_git_repo_dir_is_flagged(self) -> None:
        # Reference clones belong under .references/, not in the memory taxonomy.
        self._populate_approved()
        clone = self.memory_dir / "unknown-repo"
        clone.mkdir()
        (clone / ".git").mkdir()
        result = memory_taxonomy_message(self.root)
        self.assertIn("unknown-repo/", result)

    def test_unknown_dir_without_git_is_flagged(self) -> None:
        # A non-git directory that is not in the allowlist must produce a warning,
        # even if it would be skipped by gitignore.
        self._populate_approved()
        (self.memory_dir / "candidates").mkdir()
        result = memory_taxonomy_message(self.root)
        self.assertIn("candidates/", result)


class MemorySizeLimitTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.memory_dir = self.root / ".agents" / "memory"
        self.memory_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_memory_at_limit_produces_no_warning(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("x" * MEMORY_CHAR_LIMIT, encoding="utf-8")
        self.assertEqual(memory_health_message(self.root, {}), "")

    def test_memory_over_limit_produces_warning(self) -> None:
        (self.memory_dir / "MEMORY.md").write_text("x" * (MEMORY_CHAR_LIMIT + 1), encoding="utf-8")
        result = memory_health_message(self.root, {})
        self.assertIn("getting large", result)
        self.assertIn(str(MEMORY_CHAR_LIMIT), result)

    def test_user_at_limit_produces_no_warning(self) -> None:
        (self.memory_dir / "USER.md").write_text("x" * USER_CHAR_LIMIT, encoding="utf-8")
        self.assertEqual(user_health_message(self.root), "")

    def test_user_over_limit_produces_warning(self) -> None:
        (self.memory_dir / "USER.md").write_text("x" * (USER_CHAR_LIMIT + 1), encoding="utf-8")
        result = user_health_message(self.root)
        self.assertIn("USER.md size reminder", result)
        self.assertIn(str(USER_CHAR_LIMIT), result)

    def test_missing_memory_md_returns_notice(self) -> None:
        result = memory_health_message(self.root, {})
        self.assertIn("No MEMORY.md", result)

    def test_missing_user_md_returns_empty(self) -> None:
        self.assertEqual(user_health_message(self.root), "")


class FTS5TriggerTests(unittest.TestCase):
    def _make_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(":memory:")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                summary TEXT NOT NULL,
                body TEXT NOT NULL,
                tags TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                summary,
                body,
                content=memory_entries,
                content_rowid=id
            );
            CREATE TRIGGER IF NOT EXISTS memory_ai AFTER INSERT ON memory_entries BEGIN
                INSERT INTO memory_fts(rowid, summary, body)
                VALUES (new.id, new.summary, new.body);
            END;
            CREATE TRIGGER IF NOT EXISTS memory_ad AFTER DELETE ON memory_entries BEGIN
                INSERT INTO memory_fts(memory_fts, rowid, summary, body)
                VALUES ('delete', old.id, old.summary, old.body);
            END;
            CREATE TRIGGER IF NOT EXISTS memory_au AFTER UPDATE ON memory_entries BEGIN
                INSERT INTO memory_fts(memory_fts, rowid, summary, body)
                VALUES ('delete', old.id, old.summary, old.body);
                INSERT INTO memory_fts(rowid, summary, body)
                VALUES (new.id, new.summary, new.body);
            END;
        """)
        return conn

    def test_insert_is_searchable(self) -> None:
        conn = self._make_db()
        conn.execute("INSERT INTO memory_entries (type, summary, body) VALUES ('lesson', 'uv run usage', 'Always use uv run for Python scripts')")
        conn.commit()
        rows = conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'uv'").fetchall()
        self.assertEqual(len(rows), 1)

    def test_delete_removes_from_index(self) -> None:
        conn = self._make_db()
        conn.execute("INSERT INTO memory_entries (type, summary, body) VALUES ('lesson', 'delete me', 'temporary entry')")
        conn.commit()
        conn.execute("DELETE FROM memory_entries WHERE summary = 'delete me'")
        conn.commit()
        rows = conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'temporary'").fetchall()
        self.assertEqual(len(rows), 0)

    def test_update_reindexes_content(self) -> None:
        conn = self._make_db()
        conn.execute("INSERT INTO memory_entries (type, summary, body) VALUES ('lesson', 'old summary', 'old body content')")
        conn.commit()
        conn.execute("UPDATE memory_entries SET summary = 'new summary', body = 'new body content' WHERE summary = 'old summary'")
        conn.commit()
        old_rows = conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'old'").fetchall()
        new_rows = conn.execute("SELECT rowid FROM memory_fts WHERE memory_fts MATCH 'new'").fetchall()
        self.assertEqual(len(old_rows), 0)
        self.assertEqual(len(new_rows), 1)


if __name__ == "__main__":
    unittest.main()
