from sqlalchemy.orm import Session
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate
from app.core.exceptions import AnswerNotFoundException, QuestionNotFoundException
from app.crud import question as crud_question
from app.core.logger import get_logger

logger = get_logger("crud.answer")


def get_answer(db: Session, answer_id: int):
    logger.debug(f"Fetching answer with id {answer_id}")
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        logger.warning(f"Answer with id {answer_id} not found")
        raise AnswerNotFoundException(answer_id)
    logger.debug(f"Successfully retrieved answer with id {answer_id}")
    return answer


def create_answer(db: Session, question_id: int, answer: AnswerCreate):
    logger.info(f"Creating answer for question {question_id}")

    # Проверяем существование вопроса
    db_question = crud_question.get_question(db, question_id)
    if not db_question:
        logger.warning(f"Question with id {question_id} not found when creating answer")
        raise QuestionNotFoundException(question_id)

    db_answer = Answer(text=answer.text, user_id=answer.user_id, question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    logger.info(f"Answer created with id {db_answer.id} for question {question_id}")
    return db_answer


def delete_answer(db: Session, answer_id: int):
    logger.info(f"Deleting answer with id {answer_id}")
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not answer:
        logger.warning(f"Answer with id {answer_id} not found for deletion")
        raise AnswerNotFoundException(answer_id)
    db.delete(answer)
    db.commit()
    logger.info(f"Answer with id {answer_id} deleted successfully")
    return answer