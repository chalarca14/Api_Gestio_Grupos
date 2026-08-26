from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trabajo import Trabajo
from app.models.grupo import Grupo
from app.schemas.trabajo import TrabajoCreate, TrabajoOut, TrabajoUpdate
from app.auth import obtener_usuario_actual, requerir_rol

router = APIRouter()

# 1. Crear un trabajo o actividad (Instructor / Admin)
@router.post("/", response_model=TrabajoOut, status_code=status.HTTP_201_CREATED)
def crear_trabajo(
    trabajo: TrabajoCreate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    grupo = db.query(Grupo).filter(Grupo.id == trabajo.grupo_id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo especificado no existe."
        )

    nuevo_trabajo = Trabajo(**trabajo.model_dump())
    db.add(nuevo_trabajo)
    db.commit()
    db.refresh(nuevo_trabajo)
    return nuevo_trabajo

# 2. Listar todos los trabajos
@router.get("/", response_model=List[TrabajoOut])
def listar_trabajos(db: Session = Depends(get_db)):
    return db.query(Trabajo).all()

# 3. Obtener trabajo por ID
@router.get("/{id}", response_model=TrabajoOut)
def obtener_trabajo(id: int, db: Session = Depends(get_db)):
    trabajo = db.query(Trabajo).filter(Trabajo.id == id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado."
        )
    return trabajo

# 4. Actualizar un trabajo
@router.put("/{id}", response_model=TrabajoOut)
def actualizar_trabajo(
    id: int,
    datos_actualizados: TrabajoUpdate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    trabajo = db.query(Trabajo).filter(Trabajo.id == id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado."
        )

    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trabajo, key, value)

    db.commit()
    db.refresh(trabajo)
    return trabajo

# 5. Eliminar un trabajo por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_trabajo(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    trabajo = db.query(Trabajo).filter(Trabajo.id == id).first()
    if not trabajo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trabajo no encontrado."
        )

    db.delete(trabajo)
    db.commit()
    return None