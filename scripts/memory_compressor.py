from pathlib import Path


def count_tokens(text):
    """A very rough token estimation (characters / 4)."""
    return len(text) // 4


def main():
    memory_path = Path(".agents/memory/MEMORY.md")
    if not memory_path.exists():
        print("No MEMORY.md found.")
        return

    content = memory_path.read_text(encoding="utf-8")
    tokens = count_tokens(content)

    print("--- Memory Health Report ---")
    print(f"Approximate Tokens: {tokens}")
    print(f"Line Count: {len(content.splitlines())}")

    # Threshold Check
    if tokens > 2000 or len(content.splitlines()) > 100:
        print("\n[STATUS: VERBOSE]")
        print("Recommendation: Trigger 'compress-memory' command to summarize historical data.")
    else:
        print("\n[STATUS: LEAN]")
        print("No immediate compression required.")


if __name__ == "__main__":
    main()
