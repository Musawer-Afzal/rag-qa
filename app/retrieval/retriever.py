# core/retrieval.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self, embedder, embeddings: np.ndarray, chunks: list[str]):
        """
        embedder: SentenceTransformer or compatible model
        embeddings: numpy array of document embeddings
        chunks: original text chunks
        """
        self.embedder = embedder
        self.embeddings = embeddings
        self.chunks = chunks

    def retrieve(self, question: str, k: int = 3) -> list[str]:
        """
        Retrieve top-k most similar chunks for a question
        """
        q_emb = self.embedder.encode([question], convert_to_numpy=True)
        sims = cosine_similarity(q_emb, self.embeddings)[0]
        top_idx = sims.argsort()[-k:][::-1]
        return [self.chunks[i] for i in top_idx]