import os
from pathlib import Path


# Only files with these endings count as "code we want to search"
CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".c", ".cpp", ".h",
    ".hs", ".v", ".sql", ".html", ".css", ".md",
}

# Folders full of libraries or generated files, not your own code
SKIP_DIRS = {
    "node_modules", "venv", ".venv", ".git", "__pycache__",
    "dist", "build", ".expo", "android", "ios", ".idea", ".vscode",
}


# Huge auto-generated files that would drown out real code
SKIP_FILES = {"package-lock.json", "yarn.lock"}


def find_code_files(root):
    """Walk through a folder and return a list of code file paths"""
    root = Path(root)
    files = []
    allowed_dirs = []

    # Omit unaccepted directories from dirs to prevent OS from walking down those dirs. Improves performance
    for folder, dirs, filenames in os.walk(root):
        for d in dirs:
            if d not in SKIP_DIRS:
                allowed_dirs.append(d)

    dirs[:] = allowed_dirs

    # Build the path 
    for name in filenames:
        if name in SKIP_FILES:
            continue
        path = Path(folder) / name
        if path.suffix.lower() in CODE_EXTENSIONS:
            files.append(path)

    return files


def chunk_file(path, root, chunk_size=40, overlap=8):
    """Split one file into overlapping chunks of lines"""

    try:
        text = Path(path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return [] # Unreadable or not really text: skip it

    lines = text.splitlines()
    step = chunk_size - overlap # How far we move forward each time
    chunks = []

    for start in range(0, len(lines), step):
        piece = lines[start:start + chunk_size]
        if not "".join(piece).strip():
            continue # Skip chunks that are blank lines
        chunks.append({
            "file": Path(path).relative_to(root).as_posix(),
            "start_line": start + 1,
            "end_line": start + len(piece),
            "text": "\n".join(piece),
        })
        if start + chunk_size >= len(lines):
            break # Chunk reached end of file

    return chunks

def chunk_repo(root):
    """Find every code file under root and return all their chunks"""
    root = Path(root)
    all_chunks = []
    for path in find_code_files(root):
        all_chunks.extend(chunk_file(path, root))

    return all_chunks
            
