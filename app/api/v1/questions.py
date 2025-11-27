from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.crud import question as crud_question
from app.schemas.question import QuestionCreate, QuestionResponse
from app.dependencies.database import get_db

router = APIRouter()

@router.get("/", response_model=List[QuestionResponse])
async def read_questions(db: Session = Depends(get_db)):
    return await crud_question.get_all_questions(db)

@router.post("/", response_model=QuestionResponse)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    return await crud_question.create_question(db, question)

@router.get("/{question_id}", response_model=QuestionResponse)
async def read_question(question_id: int, db: Session = Depends(get_db)):
    return await crud_question.get_question(db, question_id)

@router.delete("/{question_id}", response_model=QuestionResponse)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    return await crud_question.delete_question(db, question_id)