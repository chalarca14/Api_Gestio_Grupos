from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CalificacionBase(BaseModel):
    nota: float = Field(..., ge=0.0, le=5.0)
    observaciones: Optional[str] = None

class CalificacionCreate(CalificacionBase):
    entrega_id: int

class CalificacionUpdate(BaseModel):
    nota: Optional[float] = Field(None, ge=0.0, le=5.0)
    observaciones: Optional[str] = None

class CalificacionOut(CalificacionBase):
    id: int
    entrega_id: int
    fecha_calificacion: datetime

    class Config:
        from_attributes = True