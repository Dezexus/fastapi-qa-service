from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import QuestionNotFoundException, AnswerNotFoundException
from app.api.v1 import questions, answers

app = FastAPI(title="Q&A API")

# Подключаем роуты
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(answers.router, prefix="/api/v1/answers", tags=["Answers"])

# Обработчики кастомных исключений
@app.exception_handler(QuestionNotFoundException)
async def question_not_found_handler(request: Request, exc: QuestionNotFoundException):
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
    return {"status": "ok"}