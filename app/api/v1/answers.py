from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import answer as crud_answer
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/{question_id}/answers/", response_model=AnswerResponse)
async def create_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    return await crud_answer.create_answer(db, question_id, answer)

@router.get("/{answer_id}", response_model=AnswerResponse)
async def read_answer(answer_id: int, db: Session = Depends(get_db)):
    return await crud_answer.get_answer(db, answer_id)

@router.delete("/{answer_id}", response_model=AnswerResponse)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    return await crud_answer.delete_answer(db, answer_id)