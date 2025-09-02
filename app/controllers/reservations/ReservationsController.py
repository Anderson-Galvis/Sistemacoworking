# controllers/reservations/ReservationsController.py
from sqlalchemy.orm import Session
from app.models.reservations.ReservationsModel import Reservation
from app.models.rooms.RoomsModel import Room
from app.models.users.UsersModel import User
from datetime import datetime, timedelta, time

from fastapi import HTTPException, status

def is_one_hour_block(hora_inicio: time, hora_fin: time):
    # asume mismos dias: diferencia de exactamente 1 hora
    dt_start = datetime.combine(datetime.today(), hora_inicio)
    dt_end = datetime.combine(datetime.today(), hora_fin)
    diff = dt_end - dt_start
    return diff == timedelta(hours=1)

def overlaps(existing_start, existing_end, new_start, new_end):
    # overlap if start < existing_end and existing_start < end
    return (new_start < existing_end) and (existing_start < new_end)

def create_reservation(db: Session, usuario_id: int, sala_id: int, fecha, hora_inicio, hora_fin):
    # validaciones
    # 1) horario 1 hora
    if not is_one_hour_block(hora_inicio, hora_fin):
        raise HTTPException(status_code=400, detail="Las reservas deben ser bloques de 1 hora exactos.")

    # 2) comprobar existencia usuario y sala
    user = db.query(User).filter(User.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    room = db.query(Room).filter(Room.id == sala_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    # 3) comprobar solapamientos para la misma sala y fecha
    existing = db.query(Reservation).filter(Reservation.sala_id == sala_id, Reservation.fecha == fecha, Reservation.estado != "cancelada").all()
    for e in existing:
        if overlaps(e.hora_inicio, e.hora_fin, hora_inicio, hora_fin):
            raise HTTPException(status_code=400, detail=f"Conflicto con reserva existente (id {e.id}).")

    # 4) crear reserva
    res = Reservation(usuario_id=usuario_id, sala_id=sala_id, fecha=fecha, hora_inicio=hora_inicio, hora_fin=hora_fin, estado="pendiente")
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_reservations_by_user(db: Session, usuario_id: int):
    return db.query(Reservation).filter(Reservation.usuario_id == usuario_id).all()

def get_reservations_by_room(db: Session, sala_id: int):
    return db.query(Reservation).filter(Reservation.sala_id == sala_id).all()

def get_reservations_by_date(db: Session, fecha):
    return db.query(Reservation).filter(Reservation.fecha == fecha).all()

def cancel_reservation(db: Session, reservation_id: int, usuario_id: int = None, force=False):
    res = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not res:
        return None
    # si no es force, solo usuario dueño o admin debería cancelarla; control en rutas
    res.estado = "cancelada"
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

# Reportes simples
def room_most_reserved(db: Session):
    from sqlalchemy import func
    q = db.query(Reservation.sala_id, func.count(Reservation.id).label("count")) \
          .group_by(Reservation.sala_id) \
          .order_by(func.count(Reservation.id).desc()) \
          .first()
    return q  # (sala_id, count) o None

def hours_reserved_by_user_month(db: Session, usuario_id: int, year: int, month: int):
    from sqlalchemy import func, extract
    total_hours = db.query(func.sum(func.timestampdiff(func.hour, Reservation.hora_inicio, Reservation.hora_fin)))\
                    .filter(Reservation.usuario_id == usuario_id, extract('year', Reservation.fecha) == year, extract('month', Reservation.fecha) == month).scalar()
    return total_hours or 0
