from typing import Optional, List
from pydantic import BaseModel

class GrupoBase(BaseModel):
    nombre: str
    codigo_ficha: str
    descripcion: Optional[str] = None

class GrupoCreate(GrupoBase):
    instructor_id: int

class GrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo_ficha: Optional[str] = None
    descripcion: Optional[str] = None
    instructor_id: Optional[int] = None

class InscripcionEstudiante(BaseModel):
    estudiante_id: int

class GrupoOut(GrupoBase):
    id: int
    instructor_id: int

    class Config:
        from_attributes = True