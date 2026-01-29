import os
import pickle
from docx import Document
from PyPDF2 import PdfReader

from core.llm_loader import load_embedder    # assuming you have a function to get embedding model



def split_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def extract_text(file_path: str) -> str:
    ext = file_path.split(".")[-1].lower()

    if ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == "docx":
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif ext == "pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_or_create_embeddings(file_path: str):
    """Load embeddings if they exist, else create from file and save."""
    base_name = os.path.basename(file_path).lower().replace(" ", "_")
    os.makedirs("data/processed", exist_ok=True)

    chunks_file = f"data/processed/{base_name}_chunks.pkl"
    embeddings_file = f"data/processed/{base_name}_embeddings.pkl"

    # If both files exist, load them
    if os.path.exists(chunks_file) and os.path.exists(embeddings_file):
        with open(chunks_file, "rb") as f:
            chunks = pickle.load(f)
        with open(embeddings_file, "rb") as f:
            embeddings = pickle.load(f)
        embedder = load_embedder()  # load embedding model
        return embeddings, chunks, embedder

    # Else, extract text and create chunks & embeddings
    text = extract_text(file_path)
    chunks = split_text(text)

    embedder = load_embedder()
    embeddings = embedder.encode(chunks, convert_to_tensor=True)

    # Save for future use
    with open(chunks_file, "wb") as f:
        pickle.dump(chunks, f)
    with open(embeddings_file, "wb") as f:
        pickle.dump(embeddings, f)

    return embeddings, chunks, embedder