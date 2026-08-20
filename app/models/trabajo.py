from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Trabajo(Base):
    __tablename__ = "trabajos"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_limite = Column(DateTime, nullable=True)

    grupo = relationship("Grupo", back_populates="trabajos")
    entregas = relationship("Entrega", back_populates="trabajo", cascade="all, delete-orphan")