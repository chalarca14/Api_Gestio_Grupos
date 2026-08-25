from pydantic import BaseModel
from typing import Optional
from app.schemas.usuario import UsuarioOut

class EstudianteBase(BaseModel):
    codigo_estudiantil: str
    documento: str

class EstudianteCreate(EstudianteBase):
    usuario_id: int

class EstudianteUpdate(BaseModel):
    codigo_estudiantil: Optional[str] = None
    documento: Optional[str] = None

class EstudianteOut(EstudianteBase):
    id: int
    usuario_id: int
    usuario: Optional[UsuarioOut] = None

    class Config:
        from_attributes = True