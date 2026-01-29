from fastapi import APIRouter, UploadFile, File, Request
import shutil
import os
import re

from core.embeddings import embed_chunks, extract_text
from retrieval.retriever import Retriever

router = APIRouter()


def normalize_filename(filename: str):
    name = filename.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w\d_]+", "", name)
    return name


@router.post("")
async def upload_document(request: Request, file: UploadFile = File(...)):
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 🔥 FIX: extract text first
    text = extract_text(file_path)

    embeddings, chunks, embedder = embed_chunks(text)

    retriever = Retriever(
        embedder=embedder,
        embeddings=embeddings,
        chunks=chunks
    )

    key = normalize_filename(file.filename)
    request.app.state.document_retrievers[key] = retriever

    return {
        "message": "Uploaded successfully",
        "doc_name": file.filename,
        "chunks": len(chunks)
    }