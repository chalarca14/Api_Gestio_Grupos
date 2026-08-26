from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EntregaBase(BaseModel):
    archivo_url: str
    comentario: Optional[str] = None

class EntregaCreate(EntregaBase):
    trabajo_id: int
    estudiante_id: int

class EntregaUpdate(BaseModel):
    archivo_url: Optional[str] = None
    comentario: Optional[str] = None

class EntregaOut(EntregaBase):
    id: int
    trabajo_id: int
    estudiante_id: int
    fecha_entrega: datetime

    class Config:
        from_attributes = True