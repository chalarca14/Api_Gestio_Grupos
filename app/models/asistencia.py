from sqlalchemy import Column, Integer, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Asistencia(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id", ondelete="CASCADE"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False)  # "asistio", "falto", "excusa"

    grupo = relationship("Grupo", back_populates="asistencias")
    estudiante = relationship("Estudiante", back_populates="asistencias")

    __table_args__ = (UniqueConstraint('grupo_id', 'estudiante_id', 'fecha', name='_grupo_estudiante_fecha_uc'),)