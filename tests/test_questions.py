def test_create_question(client):
    response = client.post("/api/v1/questions/", json={"text": "Что такое FastAPI?"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Что такое FastAPI?"
    assert "id" in data

def test_get_questions(client):
    # Создаём тестовый вопрос
    client.post("/api/v1/questions/", json={"text": "Вопрос для списка"})
    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_question_by_id(client):
    post_response = client.post("/api/v1/questions/", json={"text": "Вопрос по ID"})
    q_id = post_response.json()["id"]
    get_response = client.get(f"/api/v1/questions/{q_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == q_id

def test_delete_question(client):
    post_response = client.post("/api/v1/questions/", json={"text": "Вопрос для удаления"})
    q_id = post_response.json()["id"]
    del_response = client.delete(f"/api/v1/questions/{q_id}")
    assert del_response.status_code == 200
    # Проверка, что больше нет
    get_response = client.get(f"/api/v1/questions/{q_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_question(client):
    response = client.get("/api/v1/questions/9999")
    assert response.status_code == 404