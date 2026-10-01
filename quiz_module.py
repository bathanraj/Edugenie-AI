"""Quiz generation: 3 MCQs, 4 options each, returned as a Python list."""
import json
import re

from gemini_client import generate


def clean_json_block(text: str) -> str:
    """Strip Markdown code fences such as ```json ... ``` from a model response."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(topic_or_text: str) -> list:
    prompt = (
        "Create exactly 3 multiple-choice questions based on the topic or passage "
        "below. Each question must have exactly 4 plausible options.\n"
        "Respond ONLY with a valid JSON array, no extra text, in this format:\n"
        '[{"question": "...", "options": ["A", "B", "C", "D"], '
        '"answer": "must exactly match one of the options"}]\n\n'
        f"Topic or passage:\n{topic_or_text}"
    )
    raw = generate(prompt, json_output=True)
    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse quiz JSON: {exc}. Raw output: {raw[:300]}")

    if isinstance(data, dict):  # some responses wrap the list in an object
        data = next((v for v in data.values() if isinstance(v, list)), [])

    quiz = []
    for item in data:
        options = item.get("options", [])
        answer = item.get("answer", "")
        if len(options) == 4 and answer in options and item.get("question"):
            quiz.append({"question": item["question"], "options": options, "answer": answer})
    if not quiz:
        raise ValueError("The model did not return a valid quiz. Please try again.")
    return quiz[:3]
