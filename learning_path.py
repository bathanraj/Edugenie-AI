"""Personalized learning path with Gemini."""
from gemini_client import generate


def get_learning_recommendations(topic: str) -> str:
    prompt = (
        f"Create a structured learning path for the topic: {topic}.\n"
        "Organize it into Beginner, Intermediate and Advanced stages. For each stage "
        "give: key concepts to learn, an estimated timeline, and useful resources "
        "(videos, articles or books). Finish with 2-3 practical project ideas. "
        "Use clear headings and short bullet points."
    )
    return generate(prompt)
