from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.instructor import Instructor
from app.models.usuario import Usuario
from app.schemas.instructor import InstructorCreate, InstructorOut, InstructorUpdate
from app.auth import requerir_rol

router = APIRouter()

# 1. Crear un perfil de instructor (Solo Admin)
@router.post("/", response_model=InstructorOut, status_code=status.HTTP_201_CREATED)
def crear_instructor(
    instructor: InstructorCreate, 
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    # Verificar que el usuario base existe
    usuario = db.query(Usuario).filter(Usuario.id == instructor.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario asignado no existe."
        )

    # Verificar que el documento no esté duplicado
    existente = db.query(Instructor).filter(
        Instructor.documento == instructor.documento
    ).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento del instructor ya está registrado."
        )

    nuevo_instructor = Instructor(**instructor.model_dump())
    db.add(nuevo_instructor)
    db.commit()
    db.refresh(nuevo_instructor)
    return nuevo_instructor

# 2. Listar todos los instructores
@router.get("/", response_model=List[InstructorOut])
def listar_instructores(db: Session = Depends(get_db)):
    return db.query(Instructor).all()

# 3. Obtener instructor por ID
@router.get("/{id}", response_model=InstructorOut)
def obtener_instructor(id: int, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor no encontrado."
        )
    return instructor

# 4. Actualizar información de un instructor
@router.put("/{id}", response_model=InstructorOut)
def actualizar_instructor(
    id: int, 
    datos_actualizados: InstructorUpdate, 
    db: Session = Depends(get_db)
):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor no encontrado."
        )
    
    update_data = datos_actualizados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(instructor, key, value)
        
    db.commit()
    db.refresh(instructor)
    return instructor

# 5. Eliminar perfil de instructor (Solo Admin)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_instructor(
    id: int, 
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor no encontrado."
        )
    
    db.delete(instructor)
    db.commit()
    return None