from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EntregaBase(BaseModel):
    archivo_url: Optional[str] = None
    comentarios: Optional[str] = None

class EntregaCreate(EntregaBase):
    trabajo_id: int
    estudiante_id: int

class EntregaOut(EntregaBase):
    id: int
    trabajo_id: int
    estudiante_id: int
    fecha_entrega: datetime

    class Config:
        from_attributes = True