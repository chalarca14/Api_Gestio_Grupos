from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grupo import Grupo
from app.models.grupo_estudiante import GrupoEstudiante
from app.schemas.grupo import GrupoCreate, GrupoOut
from app.schemas.grupo_estudiante import GrupoEstudianteCreate, GrupoEstudianteOut
from app.auth import requerir_rol

router = APIRouter()

# 1. Crear un nuevo grupo (Exclusivo para Instructores/Admin)
@router.post("/", response_model=GrupoOut, status_code=status.HTTP_201_CREATED)
def crear_grupo(
    grupo: GrupoCreate, 
    db: Session = Depends(get_db),
    instructor_actual = Depends(requerir_rol("instructor"))
):
    grupo_existente = db.query(Grupo).filter(Grupo.codigo == grupo.codigo).first()
    if grupo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un grupo con ese código."
        )

    nuevo_grupo = Grupo(**grupo.model_dump())
    db.add(nuevo_grupo)
    db.commit()
    db.refresh(nuevo_grupo)
    return nuevo_grupo

# 2. Listar todos los grupos
@router.get("/", response_model=List[GrupoOut])
def listar_grupos(db: Session = Depends(get_db)):
    return db.query(Grupo).all()

# 3. Inscribir/Unir estudiante a un grupo
@router.post("/unirse", response_model=GrupoEstudianteOut, status_code=status.HTTP_201_CREATED)
def unirse_a_grupo(
    inscripcion: GrupoEstudianteCreate, 
    db: Session = Depends(get_db)
):
    inscripcion_existente = db.query(GrupoEstudiante).filter(
        GrupoEstudiante.grupo_id == inscripcion.grupo_id,
        GrupoEstudiante.estudiante_id == inscripcion.estudiante_id
    ).first()
    
    if inscripcion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante ya está inscrito en este grupo."
        )

    nueva_inscripcion = GrupoEstudiante(**inscripcion.model_dump())
    db.add(nueva_inscripcion)
    db.commit()
    db.refresh(nueva_inscripcion)
    return nueva_inscripcion