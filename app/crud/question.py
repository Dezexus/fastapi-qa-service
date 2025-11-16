from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.core.exceptions import QuestionNotFoundException
from app.core.logger import get_logger

logger = get_logger("crud.question")

def get_all_questions(db: Session):
    logger.debug("Fetching all questions")
    questions = db.query(Question).all()
    logger.info(f"Retrieved {len(questions)} questions")
    return questions

def get_question(db: Session, question_id: int):
    logger.debug(f"Fetching question with id {question_id}")
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"Question with id {question_id} not found")
        raise QuestionNotFoundException(question_id)
    logger.debug(f"Successfully retrieved question with id {question_id}")
    return question

def create_question(db: Session, question: QuestionCreate):
    logger.info(f"Creating new question: {question.text[:50]}...")
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info(f"Question created with id {db_question.id}")
    return db_question

def delete_question(db: Session, question_id: int):
    logger.info(f"Deleting question with id {question_id}")
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"Question with id {question_id} not found for deletion")
        raise QuestionNotFoundException(question_id)
    db.delete(question)
    db.commit()
    logger.info(f"Question with id {question_id} deleted successfully")
    return questionЫЫ