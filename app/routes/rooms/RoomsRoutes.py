# routes/rooms/RoomsRoutes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.deps import get_db, require_admin
from app.controllers.rooms.RoomsController import create_room, get_all_rooms, get_room_by_id, update_room, delete_room

router = APIRouter()

@router.get("/")
def list_rooms(db: Session = Depends(get_db)):
    rooms = get_all_rooms(db)
    return [{"id": r.id, "nombre": r.nombre, "sede": r.sede, "capacidad": r.capacidad, "recursos": r.recursos} for r in rooms]

@router.post("/")
def create_room_endpoint(nombre: str, sede: str, capacidad: int, recursos: str = None, admin = Depends(require_admin), db: Session = Depends(get_db)):
    room = create_room(db, nombre, sede, capacidad, recursos)
    return {"msg": "Sala creada", "room_id": room.id}

@router.put("/{room_id}")
def update_room_endpoint(room_id: int, nombre: str = None, sede: str = None, capacidad: int = None, recursos: str = None, admin = Depends(require_admin), db: Session = Depends(get_db)):
    room = update_room(db, room_id, nombre=nombre, sede=sede, capacidad=capacidad, recursos=recursos)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"msg": "Sala actualizada", "room_id": room.id}

@router.delete("/{room_id}")
def delete_room_endpoint(room_id: int, admin = Depends(require_admin), db: Session = Depends(get_db)):
    deleted = delete_room(db, room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"msg": "Sala eliminada", "room_id": room_id}
