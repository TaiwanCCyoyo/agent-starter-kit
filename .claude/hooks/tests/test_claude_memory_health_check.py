import importlib.util
import io
import json
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).parents[3]


def load_hook() -> ModuleType:
    path = ROOT / ".claude" / "hooks" / "memory_health_check.py"
    spec = importlib.util.spec_from_file_location("claude_memory_health_check", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


HOOK = load_hook()


def invoke_main(payload: object, root: Path) -> tuple[int, str]:
    stdin = io.StringIO(json.dumps(payload))
    stdout = io.StringIO()

    with (
        patch.object(HOOK.sys, "stdin", stdin),
        patch.object(HOOK.sys, "stdout", stdout),
        patch.object(HOOK, "project_root", return_value=root),
    ):
        exit_code = HOOK.main()

    return exit_code, stdout.getvalue()


def seed_clean_memory(root: Path) -> None:
    """Give MEMORY.md so memory_health_message stays quiet and other messages are isolated."""
    memory_dir = root / HOOK.MEMORY_DIR
    memory_dir.mkdir(parents=True)
    (memory_dir / "MEMORY.md").write_text("stable fact\n", encoding="utf-8")


def test_memory_health_message_fires_when_memory_md_is_oversized(tmp_path: Path) -> None:
    memory_dir = tmp_path / HOOK.MEMORY_DIR
    memory_dir.mkdir(parents=True)
    (memory_dir / "MEMORY.md").write_text("x" * (HOOK.MEMORY_CHAR_LIMIT + 1), encoding="utf-8")
    payload = {"cwd": str(tmp_path), "session_id": "s1"}

    exit_code, output = invoke_main(payload, tmp_path)

    assert exit_code == 0
    message = json.loads(output)["systemMessage"]
    assert "/compress-memory" in message


def test_memory_taxonomy_message_fires_on_unexpected_file(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    (tmp_path / HOOK.MEMORY_ROOT / "notes.txt").write_text("scratch", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "session_id": "s2"}

    exit_code, output = invoke_main(payload, tmp_path)

    assert exit_code == 0
    message = json.loads(output)["systemMessage"]
    assert "Memory taxonomy reminder" in message
    assert "notes.txt" in message


def test_no_messages_when_memory_is_clean(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    payload = {"cwd": str(tmp_path), "session_id": "s3"}

    exit_code, output = invoke_main(payload, tmp_path)

    assert exit_code == 0
    assert output == ""
