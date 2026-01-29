import os
import faiss
import pickle
import numpy as np

class FAISSStore:
    def __init__(self, dim: int, index_path: str):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = index_path + ".pkl"

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(self.meta_path, "rb") as f:
                self.chunks = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.chunks = []

    def add(self, embeddings, chunks):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.chunks.extend(chunks)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.chunks, f)

    def search(self, query_embedding, top_k=5):
        q = np.array([query_embedding]).astype("float32")
        _, indices = self.index.search(q, top_k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]