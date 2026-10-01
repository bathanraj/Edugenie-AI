"""EduGenie - FastAPI application."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

app = FastAPI(title="EduGenie", description="Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextInput(BaseModel):
    text: str


def _clean(payload: TextInput) -> str:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter some text first.")
    return text


def _run(func, text: str):
    try:
        return func(text)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/qa")
def qa(payload: TextInput):
    return {"result": _run(answer_question, _clean(payload))}


@app.post("/explain")
def explain(payload: TextInput):
    return {"result": _run(explain_concept, _clean(payload))}


@app.post("/quiz")
def quiz(payload: TextInput):
    return {"result": _run(generate_quiz, _clean(payload))}


@app.post("/summarize")
def summarize(payload: TextInput):
    return {"result": _run(summarize_text, _clean(payload))}


@app.post("/learn/recommendations")
def recommendations(payload: TextInput):
    return {"result": _run(get_learning_recommendations, _clean(payload))}
