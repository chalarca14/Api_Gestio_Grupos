from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    trabajo_id = Column(Integer, ForeignKey("trabajos.id", ondelete="CASCADE"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    archivo_url = Column(String(255), nullable=True)
    comentarios = Column(Text, nullable=True)
    fecha_entrega = Column(DateTime, default=datetime.utcnow)

    trabajo = relationship("Trabajo", back_populates="entregas")
    estudiante = relationship("Estudiante", back_populates="entregas")
    calificacion = relationship("Calificacion", back_populates="entrega", uselist=False, cascade="all, delete-orphan")