from app.db.session import SessionLocal
from app.crud.users import create_user

db = SessionLocal()

create_user(db, {"email": "admin@example.com", "password": "admin", "role": "admin"})
create_user(db, {"email": "customer@example.com", "password": "pass", "role": "customer"})
create_user(db, {"email": "courier@example.com", "password": "pass", "role": "courier"})

db.close()