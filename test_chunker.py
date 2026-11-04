import sys
from collections import Counter
from pathlib import Path

from chunker import find_code_files, chunk_repo

# Default: the Receipt Manager folder that sits next to this project.
# You can also pass a different path: python test_chunker.py "C:\some\other\folder"
default_root = Path(__file__).parent.parent / "test_Receipt-Manager"
root = Path(sys.argv[1]) if len(sys.argv) > 1 else default_root

files = find_code_files(root)
chunks = chunk_repo(root)

print(f"Scanning: {root}")
print(f"Found {len(files)} files, created {len(chunks)} chunks\n")

print("Files by type:")
for ext, count in Counter(f.suffix.lower() for f in files).most_common():
    print(f"  {ext}: {count}")

if chunks:
    sample = chunks[len(chunks) // 2]  # grab one from the middle
    print(f"\nSample chunk: {sample['file']} lines {sample['start_line']}-{sample['end_line']}")
    print("-" * 40)
    print(sample["text"])



