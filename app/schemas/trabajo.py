from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TrabajoCrear(BaseModel):
    titulo: str
    descripcion: str
    fecha_limite: datetime

class TrabajoEntregar(BaseModel):
    entregable: str

class TrabajoCertificarEstudiante(BaseModel):
    estudiante_id: int
    estado: str  # "entregado" o "no entregado"

class TrabajoRespuesta(BaseModel):
    id: int
    grupo_id: int
    titulo: str
    descripcion: str
    fecha_limite: datetime
    estado: str
    entregable: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)