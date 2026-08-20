from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    trabajo_id = Column(Integer, ForeignKey("trabajos.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    entregable = Column(String, nullable=False)
    estado = Column(String, default="entregado")  # "entregado", "aprobado", "reprobado"
    fecha_entrega = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    trabajo = relationship("Trabajo", back_populates="entregas")
    estudiante = relationship("Usuario", back_populates="entregas")