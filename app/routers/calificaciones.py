from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calificacion import Calificacion
from app.models.entrega import Entrega
from app.schemas.calificacion import (
    CalificacionCreate,
    CalificacionOut,
    CalificacionUpdate
)
from app.auth import requerir_rol

router = APIRouter()

# 1. Asignar calificación a una entrega (Instructor / Admin)
@router.post("/", response_model=CalificacionOut, status_code=status.HTTP_201_CREATED)
def crear_calificacion(
    calificacion: CalificacionCreate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    entrega = db.query(Entrega).filter(Entrega.id == calificacion.entrega_id).first()
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La entrega especificada no existe."
        )

    # Verificar si la entrega ya fue calificada
    existente = db.query(Calificacion).filter(
        Calificacion.entrega_id == calificacion.entrega_id
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta entrega ya tiene una calificación asignada."
        )

    nueva_calificacion = Calificacion(**calificacion.model_dump())
    db.add(nueva_calificacion)
    db.commit()
    db.refresh(nueva_calificacion)
    return nueva_calificacion

# 2. Listar todas las calificaciones
@router.get("/", response_model=List[CalificacionOut])
def listar_calificaciones(db: Session = Depends(get_db)):
    return db.query(Calificacion).all()

# 3. Obtener calificación por ID
@router.get("/{id}", response_model=CalificacionOut)
def obtener_calificacion(id: int, db: Session = Depends(get_db)):
    calificacion = db.query(Calificacion).filter(Calificacion.id == id).first()
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada."
        )
    return calificacion

# 4. Actualizar calificación
@router.put("/{id}", response_model=CalificacionOut)
def actualizar_calificacion(
    id: int,
    datos_actualizados: CalificacionUpdate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    calificacion = db.query(Calificacion).filter(Calificacion.id == id).first()
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada."
        )

    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(calificacion, key, value)

    db.commit()
    db.refresh(calificacion)
    return calificacion

# 5. Eliminar calificación (Solo Admin / Instructor)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_calificacion(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(requerir_rol("instructor"))
):
    calificacion = db.query(Calificacion).filter(Calificacion.id == id).first()
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada."
        )

    db.delete(calificacion)
    db.commit()
    return None