from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str

class NotificacionCreate(NotificacionBase):
    usuario_id: int

class NotificacionUpdate(BaseModel):
    leida: Optional[bool] = None

class NotificacionOut(NotificacionBase):
    id: int
    usuario_id: int
    leida: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True