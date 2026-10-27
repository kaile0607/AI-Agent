import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client()

MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
]


def generate(prompt: str) -> str:
    """Send a prompt to Gemini and return the text reply.

    Retries when a model is busy, and falls back to the next model
    if one is unavailable.
    """
    for model in MODELS:
        for attempt in range(1, 4):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text
            except errors.ServerError:
                time.sleep(2 * attempt)
            except errors.ClientError:
                break
    raise RuntimeError("All models failed. Try again later.")