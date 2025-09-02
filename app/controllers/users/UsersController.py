# controllers/users/UsersController.py
from sqlalchemy.orm import Session
from typing import List
from app.models.users.UsersModel import User
from app.utils.security import hash_password

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

def change_password(db: Session, user: User, new_password: str):
    user.contraseña_hash = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
