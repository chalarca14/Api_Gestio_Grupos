from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Trabajo(Base):
    __tablename__ = "trabajos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_entrega = Column(DateTime, nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id", ondelete="CASCADE"), nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo", back_populates="trabajos")
    entregas = relationship("Entrega", back_populates="trabajo", cascade="all, delete-orphan")