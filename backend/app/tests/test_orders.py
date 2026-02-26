from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import get_db
from app.crud.users import create_user
from app.services.orders import create_order, get_order_status, cancel_order, accept_order, start_delivery, complete_delivery

client = TestClient(app)

def test_create_order(customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post("/customers/orders", json={"from_address": "Test From", "to_address": "Test To"}, headers=headers)
    assert response.status_code == 200
    assert "order_id" in response.json()

def test_get_status(customer_token):
    # Assume order created
    db = next(get_db())
    order = create_order(db, {"from_address": "Test", "to_address": "Test"}, 1)  # user_id=1
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.get(f"/customers/orders/{order.id}/status", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_cancel_order(customer_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "Test", "to_address": "Test"}, 1)
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post(f"/customers/orders/{order.id}/cancel", headers=headers)
    assert response.status_code == 200

def test_accept_order(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "Test", "to_address": "Test"}, 1)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/accept", headers=headers)
    assert response.status_code == 200

def test_start_delivery(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "Test", "to_address": "Test"}, 1)
    accept_order(db, order.id, 2)  # courier_id=2
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/start", headers=headers)
    assert response.status_code == 200

def test_complete_delivery(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "Test", "to_address": "Test"}, 1)
    accept_order(db, order.id, 2)
    start_delivery(db, order.id, 2)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/complete", headers=headers)
    assert response.status_code == 200