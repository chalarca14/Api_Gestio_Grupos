from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrabajoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_entrega: datetime

class TrabajoCreate(TrabajoBase):
    grupo_id: int

class TrabajoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_entrega: Optional[datetime] = None

class TrabajoOut(TrabajoBase):
    id: int
    grupo_id: int
    creado_en: datetime

    class Config:
        from_attributes = True