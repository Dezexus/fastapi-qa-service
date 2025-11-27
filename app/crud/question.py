from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.core.exceptions import QuestionNotFoundException
from app.core.logger import get_logger
from app.services.cache_service import cache_service

logger = get_logger("crud.question")


async def get_all_questions(db: Session):
    # Пробуем получить из кэша
    cached_questions = await cache_service.get_cached_questions_list()
    if cached_questions:
        return cached_questions

    logger.debug("Fetching all questions from database")
    questions = db.query(Question).all()

    # Сохраняем в кэш
    questions_data = [{"id": q.id, "text": q.text, "created_at": q.created_at} for q in questions]
    await cache_service.set_cached_questions_list(questions_data)

    logger.info(f"Retrieved {len(questions)} questions")
    return questions


async def get_question(db: Session, question_id: int):
    # Пробуем получить из кэша
    cached_question = await cache_service.get_cached_question(question_id)
    if cached_question:
        return cached_question

    logger.debug(f"Fetching question with id {question_id} from database")
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"Question with id {question_id} not found")
        raise QuestionNotFoundException(question_id)

    # Сохраняем в кэш
    question_data = {
        "id": question.id,
        "text": question.text,
        "created_at": question.created_at,
        "answers": [{"id": a.id, "text": a.text, "user_id": a.user_id} for a in question.answers]
    }
    await cache_service.set_cached_question(question_id, question_data)

    logger.debug(f"Successfully retrieved question with id {question_id}")
    return question


async def create_question(db: Session, question: QuestionCreate):
    logger.info(f"Creating new question: {question.text[:50]}...")
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Инвалидируем кэш списка вопросов
    await cache_service.invalidate_questions_list()

    logger.info(f"Question created with id {db_question.id}")
    return db_question


async def delete_question(db: Session, question_id: int):
    logger.info(f"Deleting question with id {question_id}")
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"Question with id {question_id} not found for deletion")
        raise QuestionNotFoundException(question_id)

    db.delete(question)
    db.commit()

    # Инвалидируем кэш
    await cache_service.invalidate_question(question_id)
    await cache_service.invalidate_questions_list()

    logger.info(f"Question with id {question_id} deleted successfully")
    return question