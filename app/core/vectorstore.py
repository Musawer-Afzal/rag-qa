# vectorstore.py
import faiss

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.chunks = []

    def add(self, embeddings, chunks):
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding, top_k)
        return [self.chunks[i] for i in I[0]]