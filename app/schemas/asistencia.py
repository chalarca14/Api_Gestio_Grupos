from datetime import date
from typing import Optional
from pydantic import BaseModel

class AsistenciaBase(BaseModel):
    fecha: date
    estado: str  # "asistio", "falto", "excusa"
    observacion: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    estudiante_id: int
    grupo_id: int

class AsistenciaUpdate(BaseModel):
    estado: Optional[str] = None
    observacion: Optional[str] = None

class AsistenciaOut(AsistenciaBase):
    id: int
    estudiante_id: int
    grupo_id: int

    class Config:
        from_attributes = True