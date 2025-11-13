from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from app.schemas.answer import AnswerResponse

from datetime import datetime
from pydantic import BaseModel, Field, validator

class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

    @field_validator('text')
    def text_not_only_spaces(cls, value):
        if value.isspace():
            raise ValueError('Строка не должна состоять только из пробелов')
        return value

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    answers: Optional[List[AnswerResponse]] = []

    model_config = ConfigDict(from_attributes=True)
