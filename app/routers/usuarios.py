from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.auth import requerir_rol

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 1. Registro público de usuarios (Estudiantes e Instructores)
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    hashed_pwd = hash_password(usuario.password)

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        hashed_password=hashed_pwd,
        rol=usuario.rol
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

# 2. Consultar todos los usuarios (EXCLUSIVO PARA INSTRUCTORES)
@router.get("/", response_model=List[UsuarioOut], status_code=status.HTTP_200_OK)
def listar_todos_los_usuarios(
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    return db.query(Usuario).all()