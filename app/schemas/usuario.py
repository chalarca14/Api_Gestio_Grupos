from typing import Optional
from pydantic import BaseModel, EmailStr

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
    password: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioOut(UsuarioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True
        from_attributes = True