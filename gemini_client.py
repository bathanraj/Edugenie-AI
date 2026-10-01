"""Shared Gemini client used by all modules."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
_client = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


def generate(prompt: str, json_output: bool = False) -> str:
    """Send a prompt to Gemini and return the response text."""
    config = None
    if json_output:
        config = types.GenerateContentConfig(response_mime_type="application/json")
    response = get_client().models.generate_content(
        model=MODEL_NAME, contents=prompt, config=config
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("The model returned an empty response. Please try again.")
    return text
