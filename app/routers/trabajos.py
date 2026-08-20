from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trabajo import Trabajo
from app.models.grupo import Grupo
from app.models.grupo_estudiante import GrupoEstudiante
from app.models.entrega import Entrega
from app.models.usuario import Usuario
from app.schemas.trabajo import TrabajoCrear, TrabajoRespuesta
from app.auth import requerir_rol

router = APIRouter(
    prefix="/trabajos",
    tags=["Trabajos"]
)

# 1. Crear trabajo (Solo Instructores) con validación de fecha futura
@router.post("/grupo/{grupo_id}", response_model=TrabajoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_trabajo(
    grupo_id: int, 
    trabajo: TrabajoCrear, 
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    if trabajo.fecha_limite < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha límite no puede ser anterior a la fecha actual."
        )

    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="El grupo no existe.")

    nuevo_trabajo = Trabajo(
        grupo_id=grupo_id,
        titulo=trabajo.titulo,
        descripcion=trabajo.descripcion,
        fecha_limite=trabajo.fecha_limite,
        estado="activo"
    )
    db.add(nuevo_trabajo)
    db.commit()
    db.refresh(nuevo_trabajo)
    return nuevo_trabajo

# 2. Listar trabajos con PAGINACIÓN (Solo Instructores)
@router.get("/", response_model=List[TrabajoRespuesta])
def listar_todos_los_trabajos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    return db.query(Trabajo).offset(skip).limit(limit).all()

# 3. Entregar trabajo (Solo Estudiantes) - Registra en la tabla Entrega y valida fecha límite
@router.post("/{trabajo_id}/entregar", status_code=status.HTTP_201_CREATED)
def entregar_trabajo(
    trabajo_id: int,
    entregable: str,
    db: Session = Depends(get_db),
    estudiante_actual: Usuario = Depends(requerir_rol("estudiante"))
):
    trabajo = db.query(Trabajo).filter(Trabajo.id == trabajo_id).first()
    if not trabajo:
        raise HTTPException(status_code=404, detail="El trabajo no existe.")

    # Validar fecha límite
    if datetime.utcnow() > trabajo.fecha_limite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El plazo para entregar este trabajo ha expirado."
        )

    # Validar que pertenezca al grupo
    inscrito = db.query(GrupoEstudiante).filter(
        GrupoEstudiante.grupo_id == trabajo.grupo_id,
        GrupoEstudiante.estudiante_id == estudiante_actual.id
    ).first()

    if not inscrito:
        raise HTTPException(status_code=403, detail="No perteneces al grupo de esta tarea.")

    nueva_entrega = Entrega(
        trabajo_id=trabajo_id,
        estudiante_id=estudiante_actual.id,
        entregable=entregable,
        estado="entregado"
    )
    db.add(nueva_entrega)
    db.commit()
    return {"mensaje": "Trabajo entregado con éxito."}

# 4. Ver entregas por estudiante (Solo Instructores)
@router.get("/{trabajo_id}/entregas")
def ver_entregas_de_trabajo(
    trabajo_id: int,
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    return db.query(Entrega).filter(Entrega.trabajo_id == trabajo_id).all()