from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.auth import get_password_hash, requerir_rol

router = APIRouter()

# 1. Crear un nuevo usuario
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        hashed_password=get_password_hash(usuario.password),
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# 2. Listar todos los usuarios
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

# 3. Obtener un usuario por su ID
@router.get("/{id}", response_model=UsuarioOut)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return usuario

# 4. Actualizar datos de un usuario
@router.put("/{id}", response_model=UsuarioOut)
def actualizar_usuario(
    id: int, 
    datos_actualizados: UsuarioUpdate, 
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    update_data = datos_actualizados.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(usuario, key, value)
        
    db.commit()
    db.refresh(usuario)
    return usuario

# 5. Eliminar un usuario por su ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id: int, 
    db: Session = Depends(get_db),
    admin_actual = Depends(requerir_rol("admin"))
):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    db.delete(usuario)
    db.commit()
    return None