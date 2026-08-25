from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class GrupoEstudiante(Base):
    __tablename__ = "grupo_estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id", ondelete="CASCADE"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo", back_populates="estudiantes")
    estudiante = relationship("Estudiante", back_populates="grupos")

    __table_args__ = (UniqueConstraint('grupo_id', 'estudiante_id', name='_grupo_estudiante_uc'),)