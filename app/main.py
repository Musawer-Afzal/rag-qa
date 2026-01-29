# # main.py
# import os
# import re
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from core.utils import load_text, chunk_text, chunk_text_smart
# from core.embeddings import EmbeddingModel
# from core.vectorstore import VectorStore
# from app.core.llm_loader import RAGLLM

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SAMPLE_PATH = os.path.join(BASE_DIR, "../data/samples/psychology_complete_course.docx")

# # ----------------------------
# # LOAD AND CHUNK TEXT
# # ----------------------------
# print("Loading and chunking text...")
# text = load_text(SAMPLE_PATH)
# chunks = chunk_text_smart(text, chunk_size=400, overlap=50)
# print(f"Total chunks created: {len(chunks)}")

# # ----------------------------
# # EMBEDDINGS
# # ----------------------------
# print("\nGenerating embeddings...")
# embedder = EmbeddingModel()
# embeddings = embedder.embed_texts(chunks)
# print(f"Embeddings shape: {embeddings.shape}")

# # ----------------------------
# # VECTOR STORE
# # ----------------------------
# print("\nBuilding vector store...")
# store = VectorStore(dim=embeddings.shape[1])
# store.add(embeddings, chunks)

# # ----------------------------
# # EXAMPLE QUERY
# # ----------------------------
# question = "What are the Roots of Psychology?"
# # question = "What category does Employee Resistance to Change fall under?"
# print(f"\nQuestion: {question}")

# # Generate query embedding
# query_emb = embedder.embed_query(question)

# # ----------------------------
# # DEBUG: ANALYZE RETRIEVAL
# # ----------------------------
# print("\n" + "="*80)
# print("DEBUGGING RETRIEVAL - SIMILARITY ANALYSIS")
# print("="*80)

# # Calculate similarity scores for all chunks
# similarities = cosine_similarity(query_emb, embeddings)[0]

# # Show top 10 most similar chunks
# print("\nTop 10 most relevant chunks (by cosine similarity):")
# top_indices = np.argsort(similarities)[-10:][::-1]

# for i, idx in enumerate(top_indices):
#     # Clean preview text
#     chunk_preview = chunks[idx][:150].replace('\n', ' ').strip()
#     if len(chunk_preview) < len(chunks[idx]):
#         chunk_preview += "..."
    
#     print(f"\n{i+1}. Score: {similarities[idx]:.4f}")
#     print(f"   Preview: {chunk_preview}")
#     print(f"   Full length: {len(chunks[idx])} chars")

# # Also show bottom 5 for comparison
# print("\n" + "-"*80)
# print("Bottom 5 least relevant chunks:")
# bottom_indices = np.argsort(similarities)[:5]

# for i, idx in enumerate(bottom_indices):
#     chunk_preview = chunks[idx][:100].replace('\n', ' ').strip()
#     if len(chunk_preview) < len(chunks[idx]):
#         chunk_preview += "..."
    
#     print(f"\n{i+1}. Score: {similarities[idx]:.4f}")
#     print(f"   Preview: {chunk_preview}")

# # ----------------------------
# # USE TOP CHUNKS FOR CONTEXT
# # ----------------------------
# print("\n" + "="*80)
# print("BUILDING CONTEXT FROM TOP CHUNKS")
# print("="*80)

# # Use top 5 chunks instead of top 3 for better coverage
# top_k = 5
# retrieved_indices = top_indices[:top_k]
# retrieved_chunks = [chunks[idx] for idx in retrieved_indices]

# # Display retrieved chunks
# print(f"\nRetrieved top {top_k} chunks for context:")
# for i, (idx, chunk) in enumerate(zip(retrieved_indices, retrieved_chunks)):
#     print(f"\n--- Chunk {i+1} (Rank: {i+1}, Score: {similarities[idx]:.4f}, {len(chunk)} chars) ---")
#     print(chunk[:500] if len(chunk) > 500 else chunk)
#     print("-" * 50)

# # Combine chunks with better formatting
# context_parts = []
# for i, chunk in enumerate(retrieved_chunks):
#     context_parts.append(f"[Chunk {i+1}]\n{chunk}")
# context = "\n\n".join(context_parts)

# print(f"\nTotal context length: {len(context)} characters")
# print(f"Average chunk similarity score: {np.mean(similarities[retrieved_indices]):.4f}")

# # ----------------------------
# # KEYWORD SEARCH FALLBACK
# # ----------------------------
# # If semantic search fails, try keyword search
# if np.max(similarities) < 0.3:  # Low similarity threshold
#     print("\n" + "!"*80)
#     print("WARNING: Low similarity scores detected!")
#     print("Falling back to keyword search...")
#     print("!"*80)
    
#     keywords = ["roots", "history", "philosophy", "greek", "wundt", "freud", 
#                 "origins", "beginning", "historical", "milestone", "plato", "aristotle"]
    
#     keyword_chunks = []
#     for i, chunk in enumerate(chunks):
#         chunk_lower = chunk.lower()
#         matches = sum(1 for kw in keywords if kw in chunk_lower)
#         if matches >= 2:  # At least 2 keyword matches
#             keyword_chunks.append(chunk)
    
#     if keyword_chunks:
#         print(f"\nFound {len(keyword_chunks)} chunks via keyword search")
#         # Use keyword chunks instead
#         retrieved_chunks = keyword_chunks[:top_k]
#         context_parts = []
#         for i, chunk in enumerate(retrieved_chunks):
#             context_parts.append(f"[Keyword Chunk {i+1}]\n{chunk}")
#         context = "\n\n".join(context_parts)
#         print(f"New context length: {len(context)} characters")

# # ----------------------------
# # GENERATE ANSWER
# # ----------------------------
# print("\n" + "="*80)
# print("GENERATING ANSWER")
# print("="*80)
# best_chunk = retrieved_chunks[0]  # This is the "Roots of Psychology" chunk
# context = best_chunk

# # Clean it up
# context = re.sub(r'-{10,}$', '', context).strip()

# print(f"\nUsing only best chunk ({len(context)} chars):")
# print(context)

# llm = RAGLLM()
# answer = llm.generate_answer(context, question)

# print("\nQUESTION:")
# print(question)
# print("\nANSWER:")
# print(answer)

# # ----------------------------
# # ADDITIONAL DIAGNOSTICS
# # ----------------------------
# # print("\n" + "="*80)
# # print("DIAGNOSTICS")
# # print("="*80)

# # # Check if answer contains expected keywords
# # expected_keywords = ["philosophy", "greek", "wundt", "freud", "roots", "history"]
# # answer_lower = answer.lower()
# # found_keywords = [kw for kw in expected_keywords if kw in answer_lower]

# # print(f"Keywords found in answer: {found_keywords}")
# # print(f"Answer length: {len(answer)} characters")
# # print(f"Answer starts with: {answer[:100]}...")





from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.llm_loader import load_universal_model
from api.qa import router as qa_router
from api.upload import router as upload_router
from api.auth import router as auth_router

app = FastAPI(title="RAG QA System")

# ✅ CORS (REQUIRED for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("🚀 Initializing RAG system...")

    tokenizer, model = load_universal_model()

    app.state.tokenizer = tokenizer
    app.state.model = model

    # ✅ retrievers per document
    app.state.document_retrievers = {}

    print("✅ RAG system ready")

# Routers
app.include_router(upload_router, prefix="/upload")
app.include_router(qa_router, prefix="/qa")
app.include_router(auth_router, prefix="/auth")