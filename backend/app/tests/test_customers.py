from fastapi.testclient import TestClient
from app.main import app
from app.services.orders import create_order
from app.services.payments import process_payment

client = TestClient(app)

def test_create_order(customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post("/customers/orders", json={"from_address": "From", "to_address": "To"}, headers=headers)
    assert response.status_code == 200

def test_view_status(customer_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.get(f"/customers/orders/{order.id}/status", headers=headers)
    assert response.status_code == 200

def test_cancel_order(customer_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post(f"/customers/orders/{order.id}/cancel", headers=headers)
    assert response.status_code == 200

def test_pay_order(customer_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post(f"/customers/orders/{order.id}/pay", json={"number": "1234"}, headers=headers)
    assert response.status_code == 200

def test_payment_status(customer_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    process_payment(db, order.id, {"number": "1234"})
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.get(f"/customers/orders/{order.id}/payment/status", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "paid"

def test_order_history(customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.get("/customers/orders/history", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)