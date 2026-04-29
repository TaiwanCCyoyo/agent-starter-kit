import json
import sys


def main():
    # Force stdout to UTF-8 on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Read input from stdin (Gemini CLI passes hook context here)
    try:
        input_data = json.load(sys.stdin)
        # transcript_path is provided in the hook context
        transcript_path = input_data.get("transcript_path")
        if not transcript_path:
            return

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)
    except Exception:
        return

    # Check the last turn for tool calls that modify files
    # Gemini CLI transcript structure: { "turns": [ { "messages": [ ... ] } ] }
    has_modifications = False
    if "turns" in transcript and len(transcript["turns"]) > 0:
        last_turn = transcript["turns"][-1]
        for msg in last_turn.get("messages", []):
            tool_calls = msg.get("tool_calls", [])
            if tool_calls:
                for call in tool_calls:
                    # Look for tools that modify the filesystem
                    name = call.get("function", {}).get("name")
                    if name in ["write_file", "replace"]:
                        # Extract the file path from tool arguments
                        import json as json_pkg

                        args = call.get("function", {}).get("arguments", "{}")
                        if isinstance(args, str):
                            try:
                                args = json_pkg.loads(args)
                            except Exception:
                                args = {}

                        file_path = args.get("file_path", "")
                        # IGNORE changes to the memory file itself to avoid recursive loops
                        if "MEMORY.md" not in file_path:
                            has_modifications = True
                            break
            if has_modifications:
                break

    output = {}
    if has_modifications:
        # If changes detected, nudge the agent to use the proper commands or skills
        output["reason"] = (
            "System detected file modifications. Please use the 'save-memory' command OR follow the 'memory-maintenance' skill protocol "
            "to update MEMORY.md (Done & Lessons Learned) to ensure alignment with the Soul Protocol."
        )
        # Optional: systemMessage to alert the user
        output["systemMessage"] = "[System] Changes detected. Nudging agent to use 'save-memory' or 'memory-maintenance' skill."

    # Print to stdout
    print(json.dumps(output))


if __name__ == "__main__":
    main()
