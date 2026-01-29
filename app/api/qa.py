from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from core.generation import generate_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

def get_retriever(request: Request):
    return request.app.state.retriever

def get_llm(request: Request):
    return request.app.state.model, request.app.state.tokenizer

@router.post("/ask")
def ask_question(
    payload: QuestionRequest,
    retriever=Depends(get_retriever),
    llm=Depends(get_llm)
):
    model, tokenizer = llm

    context = retriever.retrieve(payload.question)
    answer = generate_answer(
        question=payload.question,
        context=context,
        model=model,
        tokenizer=tokenizer
    )

    return {
        "question": payload.question,
        "answer": answer
    }