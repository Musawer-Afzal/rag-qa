from docx import Document
from PyPDF2 import PdfReader
from core.llm_loader import load_embedder


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
        return "\n".join(p.text for p in doc.paragraphs)

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


def embed_chunks(text: str):
    """
    Extracts chunks from text and embeds them using SentenceTransformer.
    Returns:
        embeddings: np.ndarray (float32)
        chunks: list[str]
        embedder: SentenceTransformer
    """
    chunks = split_text(text)

    embedder = load_embedder()

    # FAISS requires float32 NumPy arrays
    embeddings = embedder.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings, chunks, embedder