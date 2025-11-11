from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.answer import AnswerResponse

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    answers: Optional[List[AnswerResponse]] = []

    class Config:
        orm_mode = True
