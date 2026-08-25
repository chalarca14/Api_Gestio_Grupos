from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioOut(UsuarioBase):
    id: int
    activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True