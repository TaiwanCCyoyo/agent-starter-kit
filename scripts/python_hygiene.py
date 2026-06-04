import argparse
import ast
import sys
from pathlib import Path


class PrintCallVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.findings: list[tuple[int, int]] = []

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.findings.append((node.lineno, node.col_offset + 1))
        self.generic_visit(node)


def check_no_print(filepath: str) -> list[str]:
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return []

    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{filepath}: not valid UTF-8"]
    except OSError as exc:
        return [f"{filepath}: unable to read file: {exc}"]

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return []

    visitor = PrintCallVisitor()
    visitor.visit(tree)
    return [f"{filepath}:{line}:{column}: avoid print(); use logging instead" for line, column in visitor.findings]


def main() -> int:
    parser = argparse.ArgumentParser(description="Python hygiene checks for agent and pre-commit workflows.")
    parser.add_argument("--no-print", action="store_true", help="Fail when real print(...) calls are found.")
    parser.add_argument("files", nargs="+", help="Python files to check.")
    args = parser.parse_args()

    if not args.no_print:
        parser.error("at least one check must be enabled")

    findings: list[str] = []
    for filepath in args.files:
        if Path(filepath).suffix.lower() == ".py":
            findings.extend(check_no_print(filepath))

    if findings:
        sys.stdout.write("\n".join(findings) + "\n")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
