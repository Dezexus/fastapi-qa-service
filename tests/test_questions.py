def test_create_question(client):
    response = client.post("/api/v1/questions/", json={"text": "Что такое FastAPI?"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Что такое FastAPI?"
    assert "id" in data


def test_get_questions(client):
    client.post("/api/v1/questions/", json={"text": "Вопрос 1"})
    client.post("/api/v1/questions/", json={"text": "Вопрос 2"})

    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_question_by_id(client):
    post_response = client.post("/api/v1/questions/", json={"text": "Конкретный вопрос"})
    question_id = post_response.json()["id"]

    response = client.get(f"/api/v1/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["id"] == question_id


def test_delete_question(client):
    post_response = client.post("/api/v1/questions/", json={"text": "Вопрос для удаления"})
    question_id = post_response.json()["id"]

    delete_response = client.delete(f"/api/v1/questions/{question_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_question(client):
    response = client.get("/api/v1/questions/9999")
    assert response.status_code == 404
    assert response.json()["error"] == "Question not found"


def test_delete_nonexistent_question(client):
    response = client.delete("/api/v1/questions/9999")
    assert response.status_code == 404


def test_create_question_empty_text(client):
    response = client.post("/api/v1/questions/", json={"text": "   "})
    assert response.status_code == 422


def test_create_question_too_long(client):
    long_text = "a" * 501
    response = client.post("/api/v1/questions/", json={"text": long_text})
    assert response.status_code == 422