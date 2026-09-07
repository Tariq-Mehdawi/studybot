import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import anthropic

from retrieval.hybrid import hybrid_search
from generation.answer import answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="StudyBot", description="RAG over arXiv papers")


class Question(BaseModel):
    text: str
    n_results: int = 3


class Answer(BaseModel):
    answer: str
    chunks_used: int


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
def ask(question: Question):
    if not question.text.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if question.n_results < 1 or question.n_results > 10:
        raise HTTPException(status_code=400, detail="n_results must be between 1 and 10")

    try:
        chunk_ids, chunks = hybrid_search(question.text, n_results=question.n_results)
    except Exception:
        logger.exception("Retrieval failed")
        raise HTTPException(status_code=500, detail="Retrieval failed")

    if not chunks:
        raise HTTPException(status_code=404, detail="No documents indexed")

    try:
        reply = answer(chunks, question.text)
    except anthropic.APITimeoutError:
        raise HTTPException(status_code=504, detail="Model timed out, try again")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limited, try again shortly")
    except anthropic.APIError:
        logger.exception("Anthropic API error")
        raise HTTPException(status_code=502, detail="Model unavailable")

    return Answer(answer=reply, chunks_used=len(chunks))