import sys
import re
import os

# CJK Unified Ideographs plus common CJK punctuation
CJK_RE = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')

def check_file(filepath):
    """
    Returns True if the file is clean (only English/allowed characters), 
    False otherwise.
    """
    basename = os.path.basename(filepath)
    try:
        if not os.path.exists(filepath):
            # If the file is deleted, skip it
            return True
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Special case for README.md: skip the first line (mandatory Chinese link)
            start_index = 0
            if basename.lower() == 'readme.md':
                start_index = 1
                
            for i in range(start_index, len(lines)):
                line = lines[i]
                if CJK_RE.search(line):
                    print(f"Error: Non-English (CJK) character found in {filepath} at line {i+1}:")
                    print(f"  > {line.strip()}")
                    return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    return True

def main():
    files = sys.argv[1:]
    if not files:
        print("No files to check.")
        sys.exit(0)
    
    failed = False
    for f in files:
        if not check_file(f):
            failed = True
            
    if failed:
        sys.exit(1)
    else:
        print("All English-only checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
