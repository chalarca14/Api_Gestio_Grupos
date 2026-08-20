from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo = Column(String, unique=True, index=True, nullable=False)
    instructor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # ⚠️ Esta es la propiedad que te falta definir para arreglar el error:
    instructor = relationship("Usuario", back_populates="grupos_creados")

    # Relación con Trabajos (debe coincidir con back_populates="grupo" en Trabajo)
    trabajos = relationship("Trabajo", back_populates="grupo", cascade="all, delete-orphan")