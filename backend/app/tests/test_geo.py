from fastapi.testclient import TestClient
from app.main import app
from app.services.geo import update_location

client = TestClient(app)

def test_locations(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/geo/couriers/1/locations", headers=headers)
    assert response.status_code == 200

def test_route(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/geo/couriers/1/route", headers=headers)
    assert response.status_code == 200

def test_check_fraud(admin_token):
    db = next(get_db())
    update_location(db, 1, 50.0, 30.0)
    update_location(db, 1, 50.1, 30.1)
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/geo/fraud/check/1", headers=headers)
    assert response.status_code == 200