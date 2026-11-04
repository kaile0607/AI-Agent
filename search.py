import json
from pathlib import Path

import numpy as np

from embedder import embed_texts


def load_index(index_dir="index"):
    index_dir = Path(index_dir)
    chunks = json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))
    vectors = np.load(index_dir / "vectors.npy")
    return chunks, vectors


def search(question, chunks, vectors, top_k=3):
    """Return the top_k chunks most similar in meaning to the question."""
    q = embed_texts([question], task_type="RETRIEVAL_QUERY")[0]

    # Scale every vector to length 1, so a dot product equals cosine similarity
    q = q / np.linalg.norm(q)
    normed = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    scores = normed @ q                      # one similarity score per chunk
    best = np.argsort(scores)[::-1][:top_k]  # indexes of the highest scores

    return [{**chunks[i], "score": float(scores[i])} for i in best]