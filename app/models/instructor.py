from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Instructor(Base):
    __tablename__ = "instructores"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    especialidad = Column(String(100), nullable=False)

    usuario = relationship("Usuario", back_populates="instructor")
    grupos = relationship("Grupo", back_populates="instructor")