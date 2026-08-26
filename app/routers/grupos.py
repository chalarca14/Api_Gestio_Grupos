from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grupo import Grupo
from app.models.instructor import Instructor
from app.models.estudiante import Estudiante
from app.models.grupo_estudiante import GrupoEstudiante
from app.schemas.grupo import (
    GrupoCreate,
    GrupoOut,
    GrupoUpdate,
    InscripcionEstudiante
)
from app.auth import requerir_rol

router = APIRouter()

# 1. Crear un nuevo grupo de formación (Solo Admin/Instructor)
@router.post("/", response_model=GrupoOut, status_code=status.HTTP_201_CREATED)
def crear_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    # Verificar que el instructor exista
    instructor = db.query(Instructor).filter(Instructor.id == grupo.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El instructor asignado no existe."
        )

    # Verificar código de ficha único
    existente = db.query(Grupo).filter(Grupo.codigo_ficha == grupo.codigo_ficha).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de ficha ya está registrado."
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

# 3. Obtener grupo por ID
@router.get("/{id}", response_model=GrupoOut)
def obtener_grupo(id: int, db: Session = Depends(get_db)):
    grupo = db.query(Grupo).filter(Grupo.id == id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado."
        )
    return grupo

# 4. Actualizar información de un grupo
@router.put("/{id}", response_model=GrupoOut)
def actualizar_grupo(
    id: int,
    datos_actualizados: GrupoUpdate,
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    grupo = db.query(Grupo).filter(Grupo.id == id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado."
        )

    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(grupo, key, value)

    db.commit()
    db.refresh(grupo)
    return grupo

# 5. Eliminar un grupo por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(
    id: int,
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    grupo = db.query(Grupo).filter(Grupo.id == id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado."
        )

    db.delete(grupo)
    db.commit()
    return None

# 6. Matricular/Inscribir un estudiante en un grupo (Tabla pivote)
@router.post("/{id}/matricular", status_code=status.HTTP_201_CREATED)
def matricular_estudiante(
    id: int,
    datos: InscripcionEstudiante,
    db: Session = Depends(get_db)
):
    grupo = db.query(Grupo).filter(Grupo.id == id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grupo no encontrado."
        )

    estudiante = db.query(Estudiante).filter(Estudiante.id == datos.estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )

    # Verificar si ya está matriculado
    inscripcion_existente = db.query(GrupoEstudiante).filter(
        GrupoEstudiante.grupo_id == id,
        GrupoEstudiante.estudiante_id == datos.estudiante_id
    ).first()

    if inscripcion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante ya está inscrito en este grupo."
        )

    nueva_inscripcion = GrupoEstudiante(grupo_id=id, estudiante_id=datos.estudiante_id)
    db.add(nueva_inscripcion)
    db.commit()
    return {"mensaje": f"Estudiante matriculado con éxito en el grupo {grupo.codigo_ficha}."}