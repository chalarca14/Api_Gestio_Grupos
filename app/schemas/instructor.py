from typing import Optional
from pydantic import BaseModel

class InstructorBase(BaseModel):
    especialidad: str
    documento: str

class InstructorCreate(InstructorBase):
    usuario_id: int

class InstructorUpdate(BaseModel):
    especialidad: Optional[str] = None
    documento: Optional[str] = None

class InstructorOut(InstructorBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True