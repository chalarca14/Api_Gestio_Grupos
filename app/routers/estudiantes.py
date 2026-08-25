from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.estudiante import Estudiante
from app.schemas.estudiante import EstudianteCreate, EstudianteOut

router = APIRouter()

@router.post("/", response_model=EstudianteOut, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    nuevo_estudiante = Estudiante(**estudiante.model_dump())
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

@router.get("/", response_model=List[EstudianteOut])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()