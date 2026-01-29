import os
import pickle
from fastapi import APIRouter, UploadFile, BackgroundTasks
from core.document_processor import DocumentProcessor
from core.chunking import chunk_text
from core.embeddings import EmbeddingModel

UPLOAD_DIR = "data/uploads"
PROCESSED_DIR = "data/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

router = APIRouter()

def ingest_document(file_path: str, filename: str):
    text = DocumentProcessor.load_document(file_path)
    chunks = chunk_text(text)

    embedder = EmbeddingModel()
    embeddings = embedder.embed_texts(chunks)

    with open(f"{PROCESSED_DIR}/{filename}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    with open(f"{PROCESSED_DIR}/{filename}_embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

@router.post("/upload")
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(
        ingest_document,
        file_path,
        file.filename
    )

    return {
        "filename": file.filename,
        "message": "Document uploaded and ingestion started"
    }