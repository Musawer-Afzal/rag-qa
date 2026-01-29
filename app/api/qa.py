from fastapi import APIRouter, Request
from pydantic import BaseModel
import re

router = APIRouter()

class QARequest(BaseModel):
    doc_name: str
    question: str

def normalize_filename(filename: str):
    name = filename.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w\d_]+", "", name)
    return name

@router.post("/ask")
async def ask_question(request: Request, payload: QARequest):
    key = normalize_filename(payload.doc_name)

    retrievers = request.app.state.document_retrievers
    retriever = retrievers.get(key)

    if retriever is None:
        return {"error": "Document not found. Upload first."}

    answers = retriever.retrieve(payload.question)

    return {
        "document": payload.doc_name,
        "question": payload.question,
        "answers": answers
    }