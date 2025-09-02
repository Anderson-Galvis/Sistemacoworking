# models/users/UsersModel.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="user", nullable=False)  # user / admin
    created_at = Column(DateTime, default=datetime.utcnow)