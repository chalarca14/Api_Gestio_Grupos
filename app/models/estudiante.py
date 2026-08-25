from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    codigo_estudiantil = Column(String(50), unique=True, nullable=False)
    documento = Column(String(20), unique=True, nullable=False)

    usuario = relationship("Usuario", back_populates="estudiante")
    grupos = relationship("GrupoEstudiante", back_populates="estudiante", cascade="all, delete-orphan")
    entregas = relationship("Entrega", back_populates="estudiante", cascade="all, delete-orphan")
    asistencias = relationship("Asistencia", back_populates="estudiante", cascade="all, delete-orphan")