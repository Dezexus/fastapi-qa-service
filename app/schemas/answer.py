from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict, field_validator

class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)
    user_id: str = Field(..., min_length=1, max_length=60)

    @field_validator('text')
    def text_not_only_spaces(cls, value):
        if value.isspace():
            raise ValueError('Строка не должна состоять только из пробелов')
        return value

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)