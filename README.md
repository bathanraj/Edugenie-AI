# EduGenie - Gemini Powered Learning Assistant

## Setup (VS Code)
1. Open the `EduGenie` folder in VS Code (File > Open Folder).
2. Open the terminal (Ctrl+`) and create a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your Gemini API key
   (free at https://aistudio.google.com/apikey).
5. Run: `uvicorn main:app --reload`
6. Open http://127.0.0.1:8000

## Testing
- QnA: "Which is the largest ocean?"
- Explain: "Photosynthesis"
- Quiz: "The Pythagoras Theorem" (3 MCQs; click an option to check it)
- Summarize: paste a long paragraph
- Recommend: "SQL"
- API docs / manual testing: http://127.0.0.1:8000/docs
