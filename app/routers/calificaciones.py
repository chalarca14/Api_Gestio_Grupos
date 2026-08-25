from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.calificacion import Calificacion
from app.schemas.calificacion import CalificacionCreate, CalificacionOut

router = APIRouter()

@router.post("/", response_model=CalificacionOut, status_code=status.HTTP_201_CREATED)
def crear_calificacion(calificacion: CalificacionCreate, db: Session = Depends(get_db)):
    nueva_calificacion = Calificacion(**calificacion.model_dump())
    db.add(nueva_calificacion)
    db.commit()
    db.refresh(nueva_calificacion)
    return nueva_calificacion

@router.get("/", response_model=List[CalificacionOut])
def listar_calificaciones(db: Session = Depends(get_db)):
    return db.query(Calificacion).all()