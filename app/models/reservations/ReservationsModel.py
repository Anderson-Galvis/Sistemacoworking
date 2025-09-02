# models/reservations/ReservationsModel.py
from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    fecha = Column(Date, nullable=False)         # yyyy-mm-dd
    hora_inicio = Column(Time, nullable=False)   # HH:MM:SS
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(30), default="pendiente")  # pendiente, confirmada, cancelada

    # opcional: relaciones
    # usuario = relationship("User")
    # sala = relationship("Room")
