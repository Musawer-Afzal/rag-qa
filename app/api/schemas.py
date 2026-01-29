from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str

class UploadResponse(BaseModel):
    filename: str
    message: str

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)

class AnswerResponse(BaseModel):
    answer: str