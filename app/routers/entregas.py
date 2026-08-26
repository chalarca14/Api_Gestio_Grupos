from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entrega import Entrega
from app.models.trabajo import Trabajo
from app.models.estudiante import Estudiante
from app.schemas.entrega import EntregaCreate, EntregaOut, EntregaUpdate
from app.auth import obtener_usuario_actual

router = APIRouter()

# 1. Crear / Subir una entrega
@router.post("/", response_model=EntregaOut, status_code=status.HTTP_201_CREATED)
def crear_entrega(
    entrega: EntregaCreate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    trabajo = db.query(Trabajo).filter(Trabajo.id == entrega.trabajo_id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El trabajo especificado no existe."
        )

    estudiante = db.query(Estudiante).filter(Estudiante.id == entrega.estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estudiante especificado no existe."
        )

    nueva_entrega = Entrega(**entrega.model_dump())
    db.add(nueva_entrega)
    db.commit()
    db.refresh(nueva_entrega)
    return nueva_entrega

# 2. Listar todas las entregas
@router.get("/", response_model=List[EntregaOut])
def listar_entregas(db: Session = Depends(get_db)):
    return db.query(Entrega).all()

# 3. Obtener entrega por ID
@router.get("/{id}", response_model=EntregaOut)
def obtener_entrega(id: int, db: Session = Depends(get_db)):
    entrega = db.query(Entrega).filter(Entrega.id == id).first()
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrega no encontrada."
        )
    return entrega

# 4. Actualizar una entrega
@router.put("/{id}", response_model=EntregaOut)
def actualizar_entrega(
    id: int,
    datos_actualizados: EntregaUpdate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    entrega = db.query(Entrega).filter(Entrega.id == id).first()
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrega no encontrada."
        )

    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entrega, key, value)

    db.commit()
    db.refresh(entrega)
    return entrega

# 5. Eliminar una entrega por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_entrega(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    entrega = db.query(Entrega).filter(Entrega.id == id).first()
    if not entrega:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrega no encontrada."
        )

    db.delete(entrega)
    db.commit()
    return None