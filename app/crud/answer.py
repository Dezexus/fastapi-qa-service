from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate

def get_answer(db: Session, answer_id: int):
    return db.query(Answer).filter(Answer.id == answer_id).first()

def create_answer(db: Session, question_id: int, answer: AnswerCreate):
    db_answer = Answer(text=answer.text, user_id=answer.user_id, question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer:
        db.delete(answer)
        db.commit()
    return answer
