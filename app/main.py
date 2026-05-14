from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.llm_loader import load_universal_model
from api.qa import router as qa_router
from api.upload import router as upload_router
from api.auth import router as auth_router

app = FastAPI(title="RAG QA System")

# CORS (REQUIRED for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Initializing RAG system...")

    tokenizer, model = load_universal_model()

    app.state.tokenizer = tokenizer
    app.state.model = model

    # retrievers per document
    app.state.document_retrievers = {}

    print("RAG system ready")

# Routers
app.include_router(upload_router, prefix="/upload")
app.include_router(qa_router, prefix="/qa")
app.include_router(auth_router, prefix="/auth")