from datetime import datetime
from typing import Optional
from pydantic import BaseModel

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

    class Config:
        from_attributes = True