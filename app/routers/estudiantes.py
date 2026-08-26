from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app.schemas.estudiante import EstudianteCreate, EstudianteOut, EstudianteUpdate
from app.auth import requerir_rol

router = APIRouter()

# 1. Crear un perfil de estudiante
@router.post("/", response_model=EstudianteOut, status_code=status.HTTP_201_CREATED)
def crear_estudiante(
    estudiante: EstudianteCreate, 
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    # Verificar que el usuario base existe
    usuario = db.query(Usuario).filter(Usuario.id == estudiante.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario asignado no existe."
        )

    # Verificar que el código o documento no estén duplicados
    existente = db.query(Estudiante).filter(
        (Estudiante.codigo_estudiantil == estudiante.codigo_estudiantil) |
        (Estudiante.documento == estudiante.documento)
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código estudiantil o documento ya está registrado."
        )

    nuevo_estudiante = Estudiante(**estudiante.model_dump())
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

# 2. Listar todos los estudiantes
@router.get("/", response_model=List[EstudianteOut])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# 3. Obtener estudiante por ID
@router.get("/{id}", response_model=EstudianteOut)
def obtener_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )
    return estudiante

# 4. Actualizar información de un estudiante
@router.put("/{id}", response_model=EstudianteOut)
def actualizar_estudiante(
    id: int, 
    datos_actualizados: EstudianteUpdate, 
    db: Session = Depends(get_db)
):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )
    
    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(estudiante, key, value)
        
    db.commit()
    db.refresh(estudiante)
    return estudiante

# 5. Eliminar perfil de estudiante (Exclusivo Admin)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(
    id: int, 
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado."
        )
    
    db.delete(estudiante)
    db.commit()
    return None