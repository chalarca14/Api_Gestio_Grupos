from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.instructor import Instructor
from app.schemas.instructor import InstructorCreate, InstructorOut

router = APIRouter()

@router.post("/", response_model=InstructorOut, status_code=status.HTTP_201_CREATED)
def crear_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    nuevo_instructor = Instructor(**instructor.model_dump())
    db.add(nuevo_instructor)
    db.commit()
    db.refresh(nuevo_instructor)
    return nuevo_instructor

@router.get("/", response_model=List[InstructorOut])
def listar_instructores(db: Session = Depends(get_db)):
    return db.query(Instructor).all()