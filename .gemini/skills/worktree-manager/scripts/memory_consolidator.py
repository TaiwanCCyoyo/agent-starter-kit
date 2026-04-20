import re
import sys
from pathlib import Path


def extract_section(content, section_name):
    """Extract a section from markdown content."""
    pattern = rf"## {section_name}(.*?)(?=## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        # Try finding with H3 if H2 fails (for Doing/Done)
        pattern = rf"### {section_name}(.*?)(?=## |### |\Z)"
        match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def main():
    if len(sys.argv) < 2:
        print("Usage: python memory_consolidator.py <source_path>")
        sys.exit(1)

    source_root = Path(sys.argv[1])
    target_root = Path(".").resolve()

    source_mem = source_root / ".agents" / "memory" / "MEMORY.md"

    if not source_mem.exists():
        print(f"Error: Source MEMORY.md not found at {source_mem}")
        sys.exit(1)

    print("--- Memory Consolidation Summary ---")
    print(f"Source: {source_root.name}")
    print(f"Target: {target_root.name}")

    s_content = source_mem.read_text(encoding="utf-8")

    # Extract key high-signal sections
    lessons = extract_section(s_content, "2. Lessons Learned")
    done = extract_section(s_content, "Done")

    print("\n[Extracted Lessons Learned]")
    print(lessons if lessons else "(None)")

    print("\n[Extracted Done Items]")
    print(done if done else "(None)")

    print("\n[Action Required]")
    print("Please use the 'replace' tool to append the above high-signal insights into the main MEMORY.md.")


if __name__ == "__main__":
    main()
