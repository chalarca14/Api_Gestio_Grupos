from pydantic import BaseModel
from datetime import datetime

class GrupoEstudianteCreate(BaseModel):
    grupo_id: int
    estudiante_id: int

class GrupoEstudianteOut(BaseModel):
    id: int
    grupo_id: int
    estudiante_id: int
    fecha_inscripcion: datetime

    class Config:
        from_attributes = True