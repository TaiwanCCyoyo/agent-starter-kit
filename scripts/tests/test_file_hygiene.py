import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.file_hygiene import check_file_hygiene, is_path_allowed


class FileHygieneLanguageTests(unittest.TestCase):
    def test_reference_and_temp_paths_allow_cjk(self) -> None:
        self.assertTrue(is_path_allowed(".references/hermes-agent/README.zh-CN.md"))
        self.assertTrue(is_path_allowed(".tmp/reports/implementation-report.zh-TW.md"))

    def test_memory_paths_allow_cjk(self) -> None:
        self.assertTrue(is_path_allowed(".memories/memories/USER.md"))
        self.assertTrue(is_path_allowed(".memories/memories/MEMORY.md"))

    def test_plan_marker_anywhere_in_path_allows_cjk(self) -> None:
        self.assertTrue(is_path_allowed("docs/plan/feature.md"))
        self.assertTrue(is_path_allowed("docs/plans/feature.md"))
        self.assertTrue(is_path_allowed("docs/features/feature.plan.md"))
        self.assertTrue(is_path_allowed("docs/features/implementation-plan.md"))

    def test_zh_tw_marker_anywhere_in_path_allows_cjk(self) -> None:
        self.assertTrue(is_path_allowed("docs/zh-TW/example.md"))
        self.assertTrue(is_path_allowed("docs/zh-tw/example.md"))
        self.assertTrue(is_path_allowed("docs/translations/example.zh-TW.md"))
        self.assertTrue(is_path_allowed("docs/translations/example.zh-tw.md"))

    def test_regular_english_path_does_not_allow_cjk(self) -> None:
        self.assertFalse(is_path_allowed("docs/en/example.md"))
        self.assertFalse(is_path_allowed("docs/explanation/example.md"))

    def test_allowed_path_still_requires_utf8(self) -> None:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        path = root / ".tmp" / "sample.md"
        path.parent.mkdir()
        path.write_bytes(b"\xff\xfe")

        relative = path.relative_to(root).as_posix()
        current = Path.cwd()
        try:
            os.chdir(root)
            self.assertFalse(check_file_hygiene(relative))
        finally:
            os.chdir(current)


if __name__ == "__main__":
    unittest.main()
