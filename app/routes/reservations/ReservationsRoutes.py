# routes/reservations/ReservationsRoutes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.controllers.reservations.ReservationsController import cancel_reservation

from app.utils.deps import get_db, get_current_user, require_admin
from app.controllers.reservations.ReservationsController import create_reservation, get_reservations_by_user, get_reservations_by_room, get_reservations_by_date, cancel_reservation, room_most_reserved

router = APIRouter()

@router.post("/")
def create_reservation_endpoint(sala_id: int, fecha: str, hora_inicio: str, hora_fin: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # parse fecha y horas
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_obj = datetime.strptime(hora_fin, "%H:%M").time()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de fecha/hora inválido. fecha: yyyy-mm-dd, hora: HH:MM")

    res = create_reservation(db, usuario_id=current_user.id, sala_id=sala_id, fecha=fecha_obj, hora_inicio=hora_inicio_obj, hora_fin=hora_fin_obj)
    return {"msg": "Reserva creada", "reservation_id": res.id}

@router.get("/me")
def my_reservations(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    res = get_reservations_by_user(db, current_user.id)
    return [{"id": r.id, "sala_id": r.sala_id, "fecha": str(r.fecha), "hora_inicio": r.hora_inicio.strftime("%H:%M"), "hora_fin": r.hora_fin.strftime("%H:%M"), "estado": r.estado} for r in res]

@router.get("/room/{room_id}")
def reservations_by_room(room_id: int, db: Session = Depends(get_db)):
    res = get_reservations_by_room(db, room_id)
    return [{"id": r.id, "usuario_id": r.usuario_id, "fecha": str(r.fecha), "hora_inicio": r.hora_inicio.strftime("%H:%M"), "hora_fin": r.hora_fin.strftime("%H:%M"), "estado": r.estado} for r in res]

@router.get("/date/{fecha}")
def reservations_by_date(fecha: str, db: Session = Depends(get_db)):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido, use yyyy-mm-dd")
    res = get_reservations_by_date(db, fecha_obj)
    return [{"id": r.id, "sala_id": r.sala_id, "usuario_id": r.usuario_id, "hora_inicio": r.hora_inicio.strftime("%H:%M"), "hora_fin": r.hora_fin.strftime("%H:%M"), "estado": r.estado} for r in res]

@router.delete("/{reservation_id}")
def cancel_reservation_endpoint(reservation_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    # El admin puede cancelar cualquiera; usuario solo su propia reserva
    res = db.query(__import__("models.reservations.ReservationsModel", fromlist=["Reservation"]).Reservation).filter(__import__("models.reservations.ReservationsModel", fromlist=["Reservation"]).Reservation.id == reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # si no admin y no dueño -> forbidden
    if current_user.rol != "admin" and res.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes cancelar esta reserva")
    cancel_reservation(db, reservation_id)
    return {"msg": "Reserva cancelada", "reservation_id": reservation_id}

# Reporte opcional: sala más reservada (solo admin)
@router.get("/reports/most-booked")
def report_most_booked(admin = Depends(require_admin), db: Session = Depends(get_db)):
    q = room_most_reserved(db)
    if not q:
        return {"msg": "No hay reservas"}
    sala_id, count = q
    return {"sala_id": sala_id, "reservas": count}
