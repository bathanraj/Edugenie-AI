"""Concept explanation.

Uses the local LaMini-Flan-T5-783M model when USE_LOCAL_EXPLAIN_MODEL=true,
otherwise (or if the local model can't load) falls back to Gemini.
"""
import os

from gemini_client import generate

LOCAL_MODEL_ID = "MBZUAI/LaMini-Flan-T5-783M"
_pipeline = None
_local_failed = False


def _get_local_pipeline():
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline  # imported lazily: heavy dependency

        _pipeline = pipeline("text2text-generation", model=LOCAL_MODEL_ID)
    return _pipeline


def _explain_local(topic: str) -> str:
    pipe = _get_local_pipeline()
    prompt = f"Explain the following concept in simple words for a beginner: {topic}"
    out = pipe(prompt, max_length=300, do_sample=False)
    return out[0]["generated_text"].strip()


def _explain_gemini(topic: str) -> str:
    prompt = (
        "Explain the following concept in simple, beginner-friendly language. "
        "Use a short analogy or example, and keep it under 150 words.\n\n"
        f"Concept: {topic}"
    )
    return generate(prompt)


def explain_concept(topic: str) -> str:
    global _local_failed
    use_local = os.getenv("USE_LOCAL_EXPLAIN_MODEL", "false").lower() == "true"
    if use_local and not _local_failed:
        try:
            return _explain_local(topic)
        except Exception as exc:  # missing packages, download problems, etc.
            _local_failed = True
            print(f"[EduGenie] Local model unavailable ({exc}); using Gemini instead.")
    return _explain_gemini(topic)
