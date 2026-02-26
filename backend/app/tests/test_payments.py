from fastapi.testclient import TestClient
from app.main import app
from app.services.orders import create_order

client = TestClient(app)

def test_refund(admin_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    payment_id = process_payment(db, order.id, {"number": "1234"})
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/payments/refund/{payment_id}", headers=headers)
    assert response.status_code == 200

def test_partial_refund(admin_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    payment_id = process_payment(db, order.id, {"number": "1234"})
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/payments/partial_refund/{payment_id}", json={"amount": 1.0}, headers=headers)
    assert response.status_code == 200

def test_transactions(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/payments/transactions", headers=headers)
    assert response.status_code == 200

def test_failed(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/payments/failed", headers=headers)
    assert response.status_code == 200