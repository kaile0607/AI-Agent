import json
import sys
from pathlib import Path

import numpy as np

from chunker import chunk_repo
from embedder import embed_texts

default_root = Path(__file__).parent.parent / "test_Receipt-Manager"
root = Path(sys.argv[1]) if len(sys.argv) > 1 else default_root

index_dir = Path("index")
index_dir.mkdir(exist_ok=True)

chunks = chunk_repo(root)
print(f"Chunked {len(chunks)} pieces from {root}")

# Put the file path in front of the code so the embedding knows where it came from
texts = [f"File: {c['file']}\n{c['text']}" for c in chunks]

print("Embedding... (a few seconds)")
vectors = embed_texts(texts)

(index_dir / "chunks.json").write_text(json.dumps(chunks), encoding="utf-8")
np.save(index_dir / "vectors.npy", vectors)

print(f"Saved {len(chunks)} chunks. Each vector has {vectors.shape[1]} numbers.")