# routes/users/UsersRoutes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi_jwt_auth import AuthJWT

from app.database import SessionLocal
from app.controllers.users.UsersController import get_all_users, get_user_by_id, delete_user, change_password
from app.utils.deps import get_current_user, require_admin, get_db

router = APIRouter()



@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "nombre": current_user.nombre, "email": current_user.email, "rol": current_user.rol}

@router.get("/")
def list_users(admin = Depends(require_admin), db: Session = Depends(get_db)):
    users = get_all_users(db)
    return [{"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol} for u in users]

@router.delete("/{user_id}")
def remove_user(user_id: int, admin = Depends(require_admin), db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"msg": "Usuario eliminado", "user_id": user_id}

@router.post("/change-password")
def change_pass(new_password: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = change_password(db, current_user, new_password)
    return {"msg": "Contraseña actualizada"}
