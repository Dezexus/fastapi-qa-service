def test_create_answer(client):
    # Сначала создаём вопрос
    q_response = client.post("/questions/", json={"text": "Вопрос для ответа"})
    q_id = q_response.json()["id"]

    answer_data = {"text": "Ответ на вопрос", "user_id": "user123"}
    response = client.post(f"/answers/questions/{q_id}/answers/", json=answer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Ответ на вопрос"
    assert data["question_id"] == q_id
    assert data["user_id"] == "user123"

def test_answer_to_nonexistent_question(client):
    answer_data = {"text": "Тест", "user_id": "user123"}
    response = client.post("/answers/questions/9999/answers/", json=answer_data)
    assert response.status_code == 404

def test_delete_answer(client):
    # Создаём вопрос и ответ
    q_response = client.post("/questions/", json={"text": "Вопрос для удаления ответа"})
    q_id = q_response.json()["id"]
    a_response = client.post(f"/answers/questions/{q_id}/answers/", json={"text": "Ответ", "user_id": "user123"})
    a_id = a_response.json()["id"]

    del_response = client.delete(f"/answers/{a_id}")
    assert del_response.status_code == 200
    # Проверка, что больше нет
    get_response = client.get(f"/answers/{a_id}")
    assert get_response.status_code == 404
