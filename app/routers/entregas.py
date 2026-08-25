from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.entrega import Entrega
from app.schemas.entrega import EntregaCreate, EntregaOut

router = APIRouter()

@router.post("/", response_model=EntregaOut, status_code=status.HTTP_201_CREATED)
def crear_entrega(entrega: EntregaCreate, db: Session = Depends(get_db)):
    nueva_entrega = Entrega(**entrega.model_dump())
    db.add(nueva_entrega)
    db.commit()
    db.refresh(nueva_entrega)
    return nueva_entrega

@router.get("/", response_model=List[EntregaOut])
def listar_entregas(db: Session = Depends(get_db)):
    return db.query(Entrega).all()