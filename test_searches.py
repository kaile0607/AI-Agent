import sys

from search import load_index, search

question = " ".join(sys.argv[1:]) or "where is the image upload handled?"

chunks, vectors = load_index()
results = search(question, chunks, vectors, top_k=3)

print(f"Question: {question}\n")
for r in results:
    print(f"{r['score']:.3f}  {r['file']}  lines {r['start_line']}-{r['end_line']}")
    print("-" * 50)
    print("\n".join(r["text"].splitlines()[:8]))  # first 8 lines as a preview
    print("...\n")