# controllers/rooms/RoomsController.py
from sqlalchemy.orm import Session
from app.models.rooms.RoomsModel import Room

def create_room(db: Session, nombre: str, sede: str, capacidad: int, recursos: str = None):
    room = Room(nombre=nombre, sede=sede, capacidad=capacidad, recursos=recursos)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def get_all_rooms(db: Session):
    return db.query(Room).all()

def get_room_by_id(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def update_room(db: Session, room_id: int, **kwargs):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    for k, v in kwargs.items():
        if hasattr(room, k) and v is not None:
            setattr(room, k, v)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return room
