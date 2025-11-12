from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import answer as crud_answer
from app.crud import question as crud_question
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/{question_id}/answers/", response_model=AnswerResponse)
def create_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    db_question = crud_question.get_question(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud_answer.create_answer(db, question_id, answer)

@router.get("/{answer_id}", response_model=AnswerResponse)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud_answer.get_answer(db, answer_id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer

@router.delete("/{answer_id}", response_model=AnswerResponse)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud_answer.delete_answer(db, answer_id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer
