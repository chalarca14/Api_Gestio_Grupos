from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.asistencia import Asistencia
from app.models.estudiante import Estudiante
from app.models.grupo import Grupo
from app.schemas.asistencia import (
    AsistenciaCreate,
    AsistenciaOut,
    AsistenciaUpdate
)
from app.auth import requerir_rol

router = APIRouter()

# 1. Registrar asistencia (Instructor / Admin)
@router.post("/", response_model=AsistenciaOut, status_code=status.HTTP_201_CREATED)
def registrar_asistencia(
    asistencia: AsistenciaCreate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    estudiante = db.query(Estudiante).filter(Estudiante.id == asistencia.estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estudiante especificado no existe."
        )

    grupo = db.query(Grupo).filter(Grupo.id == asistencia.grupo_id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo especificado no existe."
        )

    nueva_asistencia = Asistencia(**asistencia.model_dump())
    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)
    return nueva_asistencia

# 2. Listar todos los registros de asistencia
@router.get("/", response_model=List[AsistenciaOut])
def listar_asistencias(db: Session = Depends(get_db)):
    return db.query(Asistencia).all()

# 3. Obtener registro de asistencia por ID
@router.get("/{id}", response_model=AsistenciaOut)
def obtener_asistencia(id: int, db: Session = Depends(get_db)):
    asistencia = db.query(Asistencia).filter(Asistencia.id == id).first()
    if not asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado."
        )
    return asistencia

# 4. Actualizar estado de asistencia
@router.put("/{id}", response_model=AsistenciaOut)
def actualizar_asistencia(
    id: int,
    datos_actualizados: AsistenciaUpdate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    asistencia = db.query(Asistencia).filter(Asistencia.id == id).first()
    if not asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado."
        )

    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asistencia, key, value)

    db.commit()
    db.refresh(asistencia)
    return asistencia

# 5. Eliminar registro de asistencia (Solo Admin / Instructor)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asistencia(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    asistencia = db.query(Asistencia).filter(Asistencia.id == id).first()
    if not asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado."
        )

    db.delete(asistencia)
    db.commit()
    return None