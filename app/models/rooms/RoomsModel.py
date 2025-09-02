# models/rooms/RoomsModel.py
from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    sede = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)
    recursos = Column(JSON, nullable=True)  # almacenar como JSON-string o CSV
