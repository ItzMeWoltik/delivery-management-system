from fastapi.testclient import TestClient
from app.main import app
from app.services.orders import create_order, accept_order

client = TestClient(app)

def test_available_orders(courier_token):
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.get("/couriers/orders/available", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_accept_order(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/accept", headers=headers)
    assert response.status_code == 200

def test_decline_order(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/decline", headers=headers)
    assert response.status_code == 200

def test_start_delivery(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    accept_order(db, order.id, 2)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/start", headers=headers)
    assert response.status_code == 200

def test_complete_delivery(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    accept_order(db, order.id, 2)
    start_delivery(db, order.id, 2)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/complete", headers=headers)
    assert response.status_code == 200

def test_transfer_order(courier_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    accept_order(db, order.id, 2)
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post(f"/couriers/orders/{order.id}/transfer", json={"to_courier_id": 3}, headers=headers)
    assert response.status_code == 200

def test_active_orders(courier_token):
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.get("/couriers/orders/active", headers=headers)
    assert response.status_code == 200

def test_history(courier_token):
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.get("/couriers/orders/history", headers=headers)
    assert response.status_code == 200

def test_update_loc(courier_token):
    headers = {"Authorization": f"Bearer {courier_token}"}
    response = client.post("/couriers/location/update", json={"lat": 50.45, "lon": 30.52}, headers=headers)
    assert response.status_code == 200