import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).parents[3]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class DismissReminderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        self.state_path = self.root / ".memories" / ".claude_stop_memory_state.json"

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def _load_server(self) -> ModuleType:
        server_path = ROOT / ".claude" / "mcp" / "memory_control.py"
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(self.root)}):
            return load_module("claude_memory_control", server_path)

    def test_dismiss_resets_response_count_to_zero(self) -> None:
        self.state_path.parent.mkdir(parents=True)
        self.state_path.write_text(
            json.dumps({"session_id": "abc", "response_count": 5}),
            encoding="utf-8",
        )
        server = self._load_server()
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(self.root)}):
            result = server.dismiss_reminder()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["response_count"], 0)
        self.assertEqual(state["session_id"], "abc")
        self.assertIn("reset", result)

    def test_dismiss_creates_state_file_when_missing(self) -> None:
        server = self._load_server()
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(self.root)}):
            server.dismiss_reminder()
        self.assertTrue(self.state_path.exists())
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["response_count"], 0)

    def test_dismiss_tolerates_malformed_state_file(self) -> None:
        self.state_path.parent.mkdir(parents=True)
        self.state_path.write_text("not json", encoding="utf-8")
        server = self._load_server()
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(self.root)}):
            result = server.dismiss_reminder()
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["response_count"], 0)
        self.assertIn("reset", result)


if __name__ == "__main__":
    unittest.main()
