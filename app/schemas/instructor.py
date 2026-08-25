from pydantic import BaseModel
from typing import Optional
from app.schemas.usuario import UsuarioOut

class InstructorBase(BaseModel):
    especialidad: str

class InstructorCreate(InstructorBase):
    usuario_id: int

class InstructorUpdate(BaseModel):
    especialidad: Optional[str] = None

class InstructorOut(InstructorBase):
    id: int
    usuario_id: int
    usuario: Optional[UsuarioOut] = None

    class Config:
        from_attributes = True