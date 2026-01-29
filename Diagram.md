[User] 
   |
   |  Upload Document via /api/upload
   v
[FastAPI Upload Router]  ---> Saves to --->  [data/uploads]
   |
   |  Background processing (optional)
   v
[DocumentProcessor] ---> chunk_text() ---> [Chunks]
   |
   v
[Embeddings Module] ---> SentenceTransformer ---> [Embeddings]
   |
   v
[Processed Data Saved] ---> data/processed/  (chunks + embeddings)
   |
   |  User asks a question via /api/ask
   v
[QA Router] ---> retrieve() ---> Finds top-k relevant chunks
   |
   v
[UniversalQASystem] ---> Generates Answer using model (e.g., FLAN-T5)
   |
   v
[Answer Returned] ---> User


Project Diagram