from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import re
from app.core.exceptions import QuestionNotFoundException, AnswerNotFoundException
from app.api.v1 import questions, answers
from app.core.logger import get_logger
from app.core.redis import redis_client

# Инициализация логгера
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting up")
    await redis_client.init_redis()
    yield
    # Shutdown
    logger.info("Application shutting down")
    await redis_client.close_redis()


app = FastAPI(
    title="Q&A API",
    description="API for questions and answers with Redis caching",
    version="1.0.0",
    lifespan=lifespan
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования запросов"""
    logger.info(
        "Incoming request",
        extra={
            "extra_data": {
                "method": request.method,
                "url": str(request.url),
                "client_host": request.client.host if request.client else None
            }
        }
    )

    try:
        response = await call_next(request)
        logger.info(
            "Request completed",
            extra={
                "extra_data": {
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code
                }
            }
        )
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "extra_data": {
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e)
                }
            }
        )
        raise


# Подключаем роуты
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(answers.router, prefix="/api/v1/answers", tags=["Answers"])


# Обработчики кастомных исключений
@app.exception_handler(QuestionNotFoundException)
async def question_not_found_handler(request: Request, exc: QuestionNotFoundException):
    # Извлекаем ID вопроса из сообщения об ошибке
    question_id_match = re.search(r'id (\d+)', exc.detail)
    question_id = question_id_match.group(1) if question_id_match else None

    logger.warning(
        "Question not found",
        extra={
            "extra_data": {
                "question_id": question_id,
                "path": request.url.path
            }
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Question not found",
            "detail": exc.detail,
            "path": request.url.path
        }
    )


@app.exception_handler(AnswerNotFoundException)
async def answer_not_found_handler(request: Request, exc: AnswerNotFoundException):
    # Извлекаем ID ответа из сообщения об ошибке
    answer_id_match = re.search(r'id (\d+)', exc.detail)
    answer_id = answer_id_match.group(1) if answer_id_match else None

    logger.warning(
        "Answer not found",
        extra={
            "extra_data": {
                "answer_id": answer_id,
                "path": request.url.path
            }
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Answer not found",
            "detail": exc.detail,
            "path": request.url.path
        }
    )


@app.get("/health", tags=["Health"])
async def health_check():
    logger.debug("Health check requested")
    return {"status": "ok"}


@app.get("/", tags=["Root"])
async def root():
    logger.debug("Root endpoint accessed")
    return {
        "message": "Q&A API Service",
        "version": "1.0.0",
        "docs": "/docs"
    }