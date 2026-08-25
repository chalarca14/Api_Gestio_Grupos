from sqlalchemy import Column, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    entrega_id = Column(Integer, ForeignKey("entregas.id", ondelete="CASCADE"), unique=True, nullable=False)
    nota = Column(Float, nullable=False)
    observaciones = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    entrega = relationship("Entrega", back_populates="calificacion")