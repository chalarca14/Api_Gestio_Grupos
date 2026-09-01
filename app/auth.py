import os
from datetime import datetime, timezone, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.models.usuario import Usuario

load_dotenv()

# Configuración de variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Esquema de autenticación OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Configuración del hash de contraseñas con pwdlib
password_hash = PasswordHash((Argon2Hasher(),))

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña suministrada."""
    return password_hash.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica la contraseña ingresada con el hash almacenado."""
    return password_hash.verify(plain_password, hashed_password)

def crear_token_acceso(data: dict) -> str:
    """Crea un token JWT de acceso con tiempo de expiración."""
    a_codificar = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    a_codificar.update({"exp": expiracion})
    return jwt.encode(a_codificar, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Usuario:
    """Extrae y valida el usuario desde el token Bearer JWT."""
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise excepcion_credenciales
    except jwt.PyJWTError:
        raise excepcion_credenciales

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        raise excepcion_credenciales
    return usuario

def requerir_rol(rol_requerido: str):
    """Dependencia para restringir el acceso según el rol del usuario."""
    def verificador_rol(usuario_actual: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        if usuario_actual.rol.lower() != rol_requerido.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operación no permitida. Se requiere rol de {rol_requerido}."
            )
        return usuario_actual
    return verificador_rol