from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/dashboard", headers=headers)
    assert response.status_code == 200
    assert "live_deliveries" in response.json()

def test_alerts(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/alerts", headers=headers)
    assert response.status_code == 200

def test_apply_pause(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/admin/pauses/apply/1", json={"duration": 1, "reason": "test"}, headers=headers)
    assert response.status_code == 200

def test_all_orders(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/admin/orders", headers=headers)
    assert response.status_code == 200

def test_force_cancel(admin_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/admin/orders/{order.id}/force_cancel", headers=headers)
    assert response.status_code == 200

def test_force_complete(admin_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/admin/orders/{order.id}/force_complete", headers=headers)
    assert response.status_code == 200

def test_manual_transfer(admin_token):
    db = next(get_db())
    order = create_order(db, {"from_address": "From", "to_address": "To"}, 1)
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(f"/admin/orders/{order.id}/manual_transfer", json={"to_courier_id": 3}, headers=headers)
    assert response.status_code == 200