from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate
from app.core.exceptions import AnswerNotFoundException, QuestionNotFoundException
from app.crud import question as crud_question


def get_answer(db: Session, answer_id: int):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise AnswerNotFoundException(answer_id)
    return answer


def create_answer(db: Session, question_id: int, answer: AnswerCreate):
    # Проверяем существование вопроса
    db_question = crud_question.get_question(db, question_id)
    if not db_question:
        raise QuestionNotFoundException(question_id)

    db_answer = Answer(text=answer.text, user_id=answer.user_id, question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        raise AnswerNotFoundException(answer_id)
    db.delete(answer)
    db.commit()
    return answer