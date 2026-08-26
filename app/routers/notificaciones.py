from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.schemas.notificacion import (
    NotificacionCreate,
    NotificacionOut,
    NotificacionUpdate
)
from app.auth import obtener_usuario_actual, requerir_rol

router = APIRouter()

# 1. Crear/Enviar notificación a un usuario (Solo Admin/Instructor)
@router.post("/", response_model=NotificacionOut, status_code=status.HTTP_201_CREATED)
def crear_notificacion(
    notificacion: NotificacionCreate, 
    db: Session = Depends(get_db),
    usuario_emisor = Depends(obtener_usuario_actual)
):
    # Verificar que el usuario destinatario existe
    destinatario = db.query(Usuario).filter(Usuario.id == notificacion.usuario_id).first()
    if not destinatario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario destinatario no existe."
        )

    nueva_notificacion = Notificacion(**notificacion.model_dump())
    db.add(nueva_notificacion)
    db.commit()
    db.refresh(nueva_notificacion)
    return nueva_notificacion

# 2. Obtener todas las notificaciones (Solo Admin)
@router.get("/", response_model=List[NotificacionOut])
def listar_todas_notificaciones(
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    return db.query(Notificacion).all()

# 3. Obtener notificaciones del usuario autenticado actual
@router.get("/mis-notificaciones", response_model=List[NotificacionOut])
def obtener_mis_notificaciones(
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    return db.query(Notificacion).filter(
        Notificacion.usuario_id == usuario_actual.id
    ).all()

# 4. Marcar notificación como leída
@router.put("/{id}/marcar-leida", response_model=NotificacionOut)
def marcar_como_leida(
    id: int, 
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    notificacion = db.query(Notificacion).filter(Notificacion.id == id).first()
    if not notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada."
        )
    
    # Verificar que pertenezca al usuario autenticado o sea admin
    if notificacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta notificación."
        )
        
    notificacion.leida = True
    db.commit()
    db.refresh(notificacion)
    return notificacion

# 5. Eliminar una notificación por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_notificacion(
    id: int, 
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    notificacion = db.query(Notificacion).filter(Notificacion.id == id).first()
    if not notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada."
        )
    
    if notificacion.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta notificación."
        )

    db.delete(notificacion)
    db.commit()
    return None