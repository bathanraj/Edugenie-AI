"""Summarization with Gemini."""
from gemini_client import generate


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following educational passage into a concise, easy-to-read "
        "summary. Keep the key points, remove redundancy, and use short bullet "
        "points if it helps clarity.\n\n"
        f"Passage:\n{text}"
    )
    return generate(prompt)
