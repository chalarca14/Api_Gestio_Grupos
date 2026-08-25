from pydantic import BaseModel
from datetime import date

class AsistenciaBase(BaseModel):
    fecha: date
    estado: str  # "asistio", "falto", "excusa"

class AsistenciaCreate(AsistenciaBase):
    grupo_id: int
    estudiante_id: int

class AsistenciaOut(AsistenciaBase):
    id: int
    grupo_id: int
    estudiante_id: int

    class Config:
        from_attributes = True