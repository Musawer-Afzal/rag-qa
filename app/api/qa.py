from fastapi import APIRouter, Request
from pydantic import BaseModel
import re

router = APIRouter()

# Input model for QA
class QARequest(BaseModel):
    doc_name: str
    question: str

# Normalize filenames (same as in upload)
def normalize_filename(filename: str):
    name = filename.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w\d_]+", "", name)
    return name

# Helper to get retriever
def get_retriever(request: Request, doc_name: str):
    key = normalize_filename(doc_name)
    retrievers = getattr(request.app.state, "document_retrievers", {})
    if key not in retrievers:
        return None
    return retrievers[key]

@router.post("/ask")
async def ask_question(request: Request, payload: QARequest):
    retriever = get_retriever(request, payload.doc_name)
    if retriever is None:
        return {"error": f"Document '{payload.doc_name}' not found. Upload first."}

    # Use your RAG system to answer
    # Example: retriever.retrieve() and model.generate()
    results = retriever.retrieve(payload.question)

    return {
        "document": payload.doc_name,
        "question": payload.question,
        "answers": results
    }