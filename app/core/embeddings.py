# core/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle

def load_embeddings(
    chunks_file: str = "data/processed/psychology_chunks.pkl",
    embeddings_file: str = "data/processed/psychology_embeddings.npy",
    embedder_name: str = "all-MiniLM-L6-v2"
):
    """
    Load embeddings and chunks from disk, or compute if not exist
    Returns: embeddings, chunks, embedder
    """
    # Load chunks
    if os.path.exists(chunks_file):
        with open(chunks_file, "rb") as f:
            chunks = pickle.load(f)
    else:
        raise FileNotFoundError(f"Chunks file not found: {chunks_file}")

    # Load embeddings
    if os.path.exists(embeddings_file):
        embeddings = np.load(embeddings_file)
    else:
        # Compute embeddings if not saved
        embedder = SentenceTransformer(embedder_name)
        embeddings = embedder.encode(chunks, convert_to_numpy=True)
        np.save(embeddings_file, embeddings)
        return embeddings, chunks, embedder

    # Load embedder
    embedder = SentenceTransformer(embedder_name)

    return embeddings, chunks, embedder