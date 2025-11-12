from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    user_id: str

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
