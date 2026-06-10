import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.python_hygiene import check_no_print


class PythonHygieneTests(unittest.TestCase):
    def write_file(self, content: str) -> str:
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "sample.py"
        path.write_text(content, encoding="utf-8")
        return str(path)

    def test_flags_real_print_call(self) -> None:
        path = self.write_file("def demo():\n    print('hello')\n")

        findings = check_no_print(path)

        self.assertEqual(len(findings), 1)
        self.assertIn("avoid print(); use logging instead", findings[0])

    def test_ignores_comments_and_strings(self) -> None:
        path = self.write_file("def demo():\n    text = 'print(hello)'\n    # print('nope')\n    return text\n")

        findings = check_no_print(path)

        self.assertEqual(findings, [])

    def test_reads_utf8_source(self) -> None:
        path = self.write_file("def demo():\n    return 'cafe'\n")

        findings = check_no_print(path)

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
