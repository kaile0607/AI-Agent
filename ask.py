import sys

from rag import answer
from search import load_index

sys.stdout.reconfigure(encoding="utf-8")  # avoids Windows errors on special characters

question = " ".join(sys.argv[1:]) or "where is the image upload handled?"

chunks, vectors = load_index()
reply, sources = answer(question, chunks, vectors)

print(f"Question: {question}\n")
print(reply)

print("\nSources retrieved:")
for r in sources:
    print(f"  {r['score']:.3f}  {r['file']}  lines {r['start_line']}-{r['end_line']}")