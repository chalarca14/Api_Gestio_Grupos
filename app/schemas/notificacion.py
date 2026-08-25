from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str

class NotificacionCreate(NotificacionBase):
    usuario_id: int

class NotificacionOut(NotificacionBase):
    id: int
    usuario_id: int
    leida: bool
    creado_en: datetime

    class Config:
        from_attributes = True