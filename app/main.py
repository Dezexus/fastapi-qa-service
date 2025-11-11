from fastapi import FastAPI
from app.api.v1 import questions, answers

app = FastAPI(title="Q&A API")

# Подключаем роуты
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(answers.router, prefix="/answers", tags=["Answers"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}