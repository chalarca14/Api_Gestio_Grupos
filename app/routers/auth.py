from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
# Importa verificar_password del módulo de seguridad
from app.auth import crear_token_acceso, verificar_password

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    
    # Usa la función importada de app.auth
    if not usuario or not verificar_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo o contraseña incorrectos"
        )

    access_token = crear_token_acceso(
        data={"sub": usuario.correo, "rol": usuario.rol, "id": usuario.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}