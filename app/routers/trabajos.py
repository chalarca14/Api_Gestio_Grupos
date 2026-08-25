from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trabajo import Trabajo
from app.schemas.trabajo import TrabajoCreate, TrabajoOut
from app.auth import requerir_rol

router = APIRouter()

# 1. Crear un trabajo o actividad (Exclusivo para Instructores)
@router.post("/", response_model=TrabajoOut, status_code=status.HTTP_201_CREATED)
def crear_trabajo(
    trabajo: TrabajoCreate, 
    db: Session = Depends(get_db),
    instructor_actual = Depends(requerir_rol("instructor"))
):
    nuevo_trabajo = Trabajo(**trabajo.model_dump())
    db.add(nuevo_trabajo)
    db.commit()
    db.refresh(nuevo_trabajo)
    return nuevo_trabajo

# 2. Listar todos los trabajos registrados
@router.get("/", response_model=List[TrabajoOut])
def listar_trabajos(db: Session = Depends(get_db)):
    return db.query(Trabajo).all()

# 3. Obtener un trabajo especifico por ID
@router.get("/{id}", response_model=TrabajoOut)
def obtener_trabajo(id: int, db: Session = Depends(get_db)):
    trabajo = db.query(Trabajo).filter(Trabajo.id == id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado."
        )
    return trabajo