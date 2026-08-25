from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructores.id", ondelete="SET NULL"), nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    instructor = relationship("Instructor", back_populates="grupos")
    estudiantes = relationship("GrupoEstudiante", back_populates="grupo", cascade="all, delete-orphan")
    trabajos = relationship("Trabajo", back_populates="grupo", cascade="all, delete-orphan")
    asistencias = relationship("Asistencia", back_populates="grupo", cascade="all, delete-orphan")