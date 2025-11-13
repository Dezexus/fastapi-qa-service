from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.core.exceptions import QuestionNotFoundException

def get_all_questions(db: Session):
    return db.query(Question).all()

def get_question(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise QuestionNotFoundException(question_id)
    return question

def create_question(db: Session, question: QuestionCreate):
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise QuestionNotFoundException(question_id)
    db.delete(question)
    db.commit()
    return question