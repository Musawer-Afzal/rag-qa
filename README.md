# RAG-based Document Question Answering System

This project is a **Retrieval-Augmented Generation (RAG)** system built using **FastAPI**, **Sentence Transformers**, and **FAISS**.  
It allows users to upload documents (PDF, DOCX, TXT) and ask natural language questions based on their content.

---

## Features

- Upload documents via API or frontend
- Automatic text extraction and chunking
- Semantic embeddings using Sentence Transformers
- Fast similarity search using FAISS
- Multi-document support
- REST-based QA interface
- Simple HTML/JS frontend

---

## Architecture Overview

**Data Flow:**

1. User uploads a document
2. Text is extracted from the file
3. Text is split into overlapping chunks
4. Chunks are converted into embeddings
5. Embeddings are indexed using FAISS
6. User asks a question
7. Relevant chunks are retrieved
8. Answer is generated using retrieved context

---

## Tech Stack

- **Backend:** FastAPI
- **Embeddings:** SentenceTransformers
- **Vector Store:** FAISS
- **LLM:** Hugging Face Transformer
- **Frontend:** HTML, CSS, JavaScript

---

## Setup Instructions

### Clone the Repository
```bash
git clone <your-github-repo-link>
cd rag-qa
