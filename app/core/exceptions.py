from fastapi import HTTPException, status

class QuestionNotFoundException(HTTPException):
    def __init__(self, question_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )

class AnswerNotFoundException(HTTPException):
    def __init__(self, answer_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Answer with id {answer_id} not found"
        )

class EmptyContentException(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field} cannot be empty"
        )