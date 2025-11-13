def test_create_answer(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос для ответа"})
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": "Тестовый ответ", "user_id": "user-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Тестовый ответ"
    assert data["question_id"] == question_id


def test_create_answer_nonexistent_question(client):
    response = client.post(
        "/api/v1/answers/9999/answers/",
        json={"text": "Ответ", "user_id": "user-123"}
    )
    assert response.status_code == 404


def test_get_answer(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос"})
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": "Ответ", "user_id": "user-123"}
    )
    answer_id = answer_response.json()["id"]

    response = client.get(f"/api/v1/answers/{answer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == answer_id


def test_delete_answer(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос"})
    question_id = question_response.json()["id"]

    answer_response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": "Ответ для удаления", "user_id": "user-123"}
    )
    answer_id = answer_response.json()["id"]

    delete_response = client.delete(f"/api/v1/answers/{answer_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/v1/answers/{answer_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_answer(client):
    response = client.get("/api/v1/answers/9999")
    assert response.status_code == 404
    assert response.json()["error"] == "Answer not found"


def test_delete_nonexistent_answer(client):
    response = client.delete("/api/v1/answers/9999")
    assert response.status_code == 404


def test_create_answer_empty_text(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос"})
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": "   ", "user_id": "user-123"}
    )
    assert response.status_code == 422


def test_create_answer_too_long(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос"})
    question_id = question_response.json()["id"]

    long_text = "a" * 1001
    response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": long_text, "user_id": "user-123"}
    )
    assert response.status_code == 422


def test_create_answer_empty_user_id(client):
    question_response = client.post("/api/v1/questions/", json={"text": "Вопрос"})
    question_id = question_response.json()["id"]

    response = client.post(
        f"/api/v1/answers/{question_id}/answers/",
        json={"text": "Ответ", "user_id": ""}
    )
    assert response.status_code == 422