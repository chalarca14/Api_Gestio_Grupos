from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.asistencia import Asistencia
from app.schemas.asistencia import AsistenciaCreate, AsistenciaOut

router = APIRouter()

@router.post("/", response_model=AsistenciaOut, status_code=status.HTTP_201_CREATED)
def registrar_asistencia(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
    nueva_asistencia = Asistencia(**asistencia.model_dump())
    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)
    return nueva_asistencia

@router.get("/", response_model=List[AsistenciaOut])
def listar_asistencias(db: Session = Depends(get_db)):
    return db.query(Asistencia).all()