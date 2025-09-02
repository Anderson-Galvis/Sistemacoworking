# controllers/auth/AuthController.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from app.database import SessionLocal
from app.models.users.UsersModel import User
from app.utils.security import hash_password, verify_password

router = APIRouter()

class RegisterSchema(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str
    rol: str = "user"

class LoginSchema(BaseModel):
    email: EmailStr
    contraseña: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", summary="Registrar usuario")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = User(
        nombre=data.nombre,
        email=data.email,
        contraseña_hash=hash_password(data.contraseña),
        rol=data.rol
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "Usuario creado", "user_id": user.id}

@router.post("/login", summary="Login y generar JWT")
def login(data: LoginSchema, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.contraseña, user.contraseña_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = Authorize.create_access_token(subject=str(user.id))
    refresh_token = Authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "user": {"id": user.id, "nombre": user.nombre, "email": user.email, "rol": user.rol}}

@router.post("/refresh", summary="Refresh token")
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    current_user = Authorize.get_jwt_subject()
    new_access = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access}
