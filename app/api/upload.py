from fastapi import APIRouter, UploadFile, File, Request
import shutil
import os
import re

from core.embeddings import load_or_create_embeddings
from retrieval.retriever import Retriever

router = APIRouter()

def normalize_filename(filename: str):
    name = filename.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w\d_]+", "", name)
    return name


@router.post("/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        embeddings, chunks, embedder = load_or_create_embeddings(file_path)
    except ValueError as e:
        return {"error": str(e)}

    retriever = Retriever(
        embedder=embedder,
        embeddings=embeddings,
        chunks=chunks
    )

    # ✅ Initialize storage once
    if not hasattr(request.app.state, "document_retrievers"):
        request.app.state.document_retrievers = {}

    key = normalize_filename(file.filename)

    # ✅ Store retriever correctly
    request.app.state.document_retrievers[key] = retriever

    return {
        "message": f"Document '{file.filename}' uploaded and retriever created.",
        "doc_key": key
    }