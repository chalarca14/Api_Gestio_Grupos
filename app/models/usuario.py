from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)

    # Coincide con back_populates="instructor" en Grupo
    grupos_creados = relationship("Grupo", back_populates="instructor")
    
    # Coincide con back_populates="estudiante" en Entrega
    entregas = relationship("Entrega", back_populates="estudiante")