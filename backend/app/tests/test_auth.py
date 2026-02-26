from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings
from app.crud.users import create_user

client = TestClient(app)

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def setup_module():
    Base.metadata.create_all(bind=test_engine)

def teardown_module():
    Base.metadata.drop_all(bind=test_engine)

def test_register():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "pass", "role": "customer"})
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_login_success():
    # Assume registered
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    response = client.post("/auth/login", json={"email": "wrong@example.com", "password": "wrong"})
    assert response.status_code == 401

def test_logout():
    login_resp = client.post("/auth/login", json={"email": "test@example.com", "password": "pass"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

def test_refresh():
    login_resp = client.post("/auth/login", json={"email": "test@example.com", "password": "pass"})
    refresh_token = login_resp.json()["refresh_token"]
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_delete_user():
    # Create admin
    db = TestingSessionLocal()
    admin = create_user(db, {"email": "admin@test.com", "password": "admin", "role": "admin"})
    db.close()
    admin_login = client.post("/auth/login", json={"email": "admin@test.com", "password": "admin"})
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = client.post("/auth/register", json={"email": "delete@test.com", "password": "pass", "role": "customer"})
    user_id = user_resp.json()["user_id"]
    response = client.delete(f"/auth/delete/{user_id}", headers=headers)
    assert response.status_code == 200