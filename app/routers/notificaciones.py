from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.notificacion import Notificacion
from app.schemas.notificacion import NotificacionCreate, NotificacionOut

router = APIRouter()

@router.post("/", response_model=NotificacionOut, status_code=status.HTTP_201_CREATED)
def crear_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    nueva_notificacion = Notificacion(**notificacion.model_dump())
    db.add(nueva_notificacion)
    db.commit()
    db.refresh(nueva_notificacion)
    return nueva_notificacion

@router.get("/", response_model=List[NotificacionOut])
def listar_notificaciones(db: Session = Depends(get_db)):
    return db.query(Notificacion).all()