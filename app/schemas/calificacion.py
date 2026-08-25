from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalificacionBase(BaseModel):
    nota: float
    observaciones: Optional[str] = None

class CalificacionCreate(CalificacionBase):
    entrega_id: int

class CalificacionUpdate(BaseModel):
    nota: Optional[float] = None
    observaciones: Optional[str] = None

class CalificacionOut(CalificacionBase):
    id: int
    entrega_id: int
    creado_en: datetime

    class Config:
        from_attributes = True