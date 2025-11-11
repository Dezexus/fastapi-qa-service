from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate

def get_all_questions(db: Session):
    return db.query(Question).all()

def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def create_question(db: Session, question: QuestionCreate):
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        db.delete(question)
        db.commit()
    return question
