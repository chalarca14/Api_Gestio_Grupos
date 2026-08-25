from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GrupoBase(BaseModel):
    nombre: str
    codigo: str

class GrupoCreate(GrupoBase):
    instructor_id: Optional[int] = None

class GrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    instructor_id: Optional[int] = None

class GrupoOut(GrupoBase):
    id: int
    instructor_id: Optional[int] = None
    creado_en: datetime

    class Config:
        from_attributes = True