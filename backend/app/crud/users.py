from sqlalchemy.orm import Session
from app.db.models.users import User
from app.core.security import hash_password, verify_password
from .base import CRUDBase

class CRUDUser(CRUDBase[User]):
    def create(self, db: Session, obj_in: dict):
        obj_in['hashed_password'] = hash_password(obj_in.pop('password'))
        return super().create(db, obj_in)

    def authenticate(self, db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def soft_delete(self, db: Session, user_id: int):
        user = self.get(db, user_id)
        if user:
            user.is_active = False
            db.commit()

user = CRUDUser(User)
create_user = user.create
authenticate_user = user.authenticate
soft_delete_user = user.soft_delete