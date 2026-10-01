"""Question answering with Gemini."""
from gemini_client import generate


def answer_question(question: str) -> str:
    prompt = (
        "You are EduGenie, a friendly educational assistant. Answer the student's "
        "question accurately and concisely (2-5 sentences unless more detail is "
        "clearly needed). Use plain language.\n\n"
        f"Question: {question}"
    )
    return generate(prompt)
