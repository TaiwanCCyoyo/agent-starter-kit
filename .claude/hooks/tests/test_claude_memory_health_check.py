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


def invoke_main(payload: object, root: Path, now: float) -> tuple[int, str]:
    stdin = io.StringIO(json.dumps(payload))
    stdout = io.StringIO()

    with (
        patch.object(HOOK.sys, "stdin", stdin),
        patch.object(HOOK.sys, "stdout", stdout),
        patch.object(HOOK, "project_root", return_value=root),
        patch.object(HOOK.time, "time", return_value=now),
    ):
        exit_code = HOOK.main()

    return exit_code, stdout.getvalue()


def learn_eval_state_path(root: Path) -> Path:
    return root / HOOK.LEARN_EVAL_STATE_FILE


def seed_clean_memory(root: Path) -> None:
    """Give MEMORY.md so memory_health_message stays quiet and the reminder message is isolated."""
    memory_dir = root / HOOK.MEMORY_DIR
    memory_dir.mkdir(parents=True)
    (memory_dir / "MEMORY.md").write_text("stable fact\n", encoding="utf-8")


def test_learn_eval_reminder_fires_on_first_run(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    payload = {"cwd": str(tmp_path), "session_id": "s1"}

    exit_code, output = invoke_main(payload, tmp_path, now=1_000_000.0)

    assert exit_code == 0
    message = json.loads(output)["systemMessage"]
    assert "/learn-eval" in message
    assert "/memory-maintenance" in message
    state = json.loads(learn_eval_state_path(tmp_path).read_text(encoding="utf-8"))
    assert state["last_reminder_at"] == 1_000_000.0


def test_learn_eval_reminder_suppressed_within_interval(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    learn_eval_state_path(tmp_path).write_text(json.dumps({"last_reminder_at": 1_000_000.0}), encoding="utf-8")
    payload = {"cwd": str(tmp_path), "session_id": "s2"}

    exit_code, output = invoke_main(payload, tmp_path, now=1_000_000.0 + 60)

    assert exit_code == 0
    assert output == ""


def test_learn_eval_reminder_fires_again_after_interval_elapses(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    learn_eval_state_path(tmp_path).write_text(json.dumps({"last_reminder_at": 1_000_000.0}), encoding="utf-8")
    payload = {"cwd": str(tmp_path), "session_id": "s3"}

    exit_code, output = invoke_main(payload, tmp_path, now=1_000_000.0 + HOOK.LEARN_EVAL_REMINDER_INTERVAL_SECONDS + 1)

    assert exit_code == 0
    message = json.loads(output)["systemMessage"]
    assert "/learn-eval" in message


def test_learn_eval_reminder_survives_corrupt_state_file(tmp_path: Path) -> None:
    seed_clean_memory(tmp_path)
    learn_eval_state_path(tmp_path).write_text("{not-json", encoding="utf-8")
    payload = {"cwd": str(tmp_path), "session_id": "s4"}

    exit_code, output = invoke_main(payload, tmp_path, now=1_000_000.0)

    assert exit_code == 0
    message = json.loads(output)["systemMessage"]
    assert "/learn-eval" in message
