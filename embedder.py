import time

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client()

EMBED_MODEL = "gemini-embedding-001"
BATCH_SIZE = 50  # how many texts to send per request


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):
    """Turn a list of texts into a 2D numpy array: one vector per text."""
    vectors = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]

        for attempt in range(1, 6):
            try:
                response = client.models.embed_content(
                    model=EMBED_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(task_type=task_type),
                )
                vectors.extend(e.values for e in response.embeddings)
                break
            except errors.ServerError:
                time.sleep(2 * attempt)  # server busy: wait and retry
            except errors.ClientError as e:
                if e.code == 429:
                    time.sleep(10 * attempt)  # rate limit: wait longer
                else:
                    raise  # a real mistake (bad model name, etc.)
        else:
            raise RuntimeError("Embedding failed after 5 attempts.")

    return np.array(vectors, dtype=np.float32)