from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.users import UserCreate, UserLogin
from app.crud.users import create_user, authenticate_user, soft_delete_user
from app.core.security import create_access_token, create_refresh_token, blacklist_token
from app.utils.logging import log_action

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    log_action(f"User registered: {db_user.id}")
    return {"msg": "Registered", "user_id": db_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(db_user.id)
    refresh_token = create_refresh_token(db_user.id)
    log_action(f"User logged in: {db_user.id}")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    blacklist_token(token)
    return {"msg": "Logged out"}

@router.post("/refresh")
def refresh(refresh_token: str):
    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = create_access_token(user_id)
    return {"access_token": access_token}

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    soft_delete_user(db, user_id)
    return {"msg": "User soft deleted"}