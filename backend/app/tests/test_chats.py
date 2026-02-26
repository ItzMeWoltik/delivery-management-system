from fastapi.testclient import TestClient
from app.main import app
from app.crud.chats import create_message, create_ticket

client = TestClient(app)

def test_send_message(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/chats/messages", json={"chat_id": 1, "content": "Test message"}, headers=headers)
    assert response.status_code == 200

def test_chat_history(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/chats/chats/1/history", headers=headers)
    assert response.status_code == 200

def test_create_ticket(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/chats/tickets", json={"description": "Test ticket"}, headers=headers)
    assert response.status_code == 200

def test_ticket_status(user_token):
    db = next(get_db())
    ticket_id = create_ticket(db, {"description": "Test"}, 1)
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/chats/tickets/{ticket_id}/status", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "open"