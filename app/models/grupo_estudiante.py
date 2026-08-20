from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class GrupoEstudiante(Base):
    __tablename__ = "grupo_estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)