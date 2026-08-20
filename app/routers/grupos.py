import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grupo import Grupo
from app.models.grupo_estudiante import GrupoEstudiante
from app.models.usuario import Usuario
from app.schemas.grupo import GrupoCrear, GrupoRespuesta, UnirseGrupo
from app.schemas.usuario import UsuarioRespuesta
from app.auth import requerir_rol, obtener_usuario_actual

router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"]
)

def generar_codigo_unico() -> str:
    return str(uuid.uuid4())[:6].upper()

# 1. Crear grupo (Solo Instructores)
@router.post("/", response_model=GrupoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_grupo(
    grupo: GrupoCrear, 
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    codigo = generar_codigo_unico()
    
    nuevo_grupo = Grupo(
        nombre=grupo.nombre,
        codigo=codigo,
        instructor_id=instructor_actual.id
    )
    
    db.add(nuevo_grupo)
    db.commit()
    db.refresh(nuevo_grupo)
    return nuevo_grupo

# 2. Consultar TODOS los grupos (Solo Instructores)
@router.get("/", response_model=List[GrupoRespuesta], status_code=status.HTTP_200_OK)
def listar_todos_los_grupos(
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    return db.query(Grupo).all()

# 3. Consultar los grupos CREADOS POR EL INSTRUCTOR actual
@router.get("/mis-grupos-instructor", response_model=List[GrupoRespuesta], status_code=status.HTTP_200_OK)
def listar_mis_grupos_instructor(
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    return db.query(Grupo).filter(Grupo.instructor_id == instructor_actual.id).all()

# 4. Consultar los estudiantes de un grupo específico (Solo Instructores)
@router.get("/{grupo_id}/estudiantes", response_model=List[UsuarioRespuesta], status_code=status.HTTP_200_OK)
def listar_estudiantes_de_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    instructor_actual: Usuario = Depends(requerir_rol("instructor"))
):
    # Verificar que el grupo exista
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El grupo especificado no existe."
        )
    
    # Opcional: Validar que el instructor que consulta sea el dueño del grupo
    if grupo.instructor_id != instructor_actual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los estudiantes de este grupo."
        )

    # Consulta con JOIN a través de la tabla intermedia GrupoEstudiante
    estudiantes = db.query(Usuario).join(
        GrupoEstudiante, Usuario.id == GrupoEstudiante.estudiante_id
    ).filter(
        GrupoEstudiante.grupo_id == grupo_id
    ).all()

    return estudiantes

# 5. Consultar los grupos DONDE ESTÁ INSCRITO un estudiante
@router.get("/mis-grupos-estudiante", response_model=List[GrupoRespuesta], status_code=status.HTTP_200_OK)
def listar_mis_grupos_estudiante(
    db: Session = Depends(get_db),
    estudiante_actual: Usuario = Depends(requerir_rol("estudiante"))
):
    return db.query(Grupo).join(
        GrupoEstudiante, Grupo.id == GrupoEstudiante.grupo_id
    ).filter(
        GrupoEstudiante.estudiante_id == estudiante_actual.id
    ).all()

# 6. Unirse a un grupo (Solo Estudiantes)
@router.post("/unirse", status_code=status.HTTP_200_OK)
def unirse_a_grupo(
    datos: UnirseGrupo, 
    db: Session = Depends(get_db),
    estudiante_actual: Usuario = Depends(requerir_rol("estudiante"))
):
    grupo = db.query(Grupo).filter(Grupo.codigo == datos.codigo).first()
    if not grupo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de grupo inválido."
        )

    inscripcion_existente = db.query(GrupoEstudiante).filter(
        GrupoEstudiante.grupo_id == grupo.id,
        GrupoEstudiante.estudiante_id == estudiante_actual.id
    ).first()

    if inscripcion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya estás inscrito en este grupo."
        )

    nueva_inscripcion = GrupoEstudiante(
        grupo_id=grupo.id,
        estudiante_id=estudiante_actual.id
    )
    db.add(nueva_inscripcion)
    db.commit()

    return {"mensaje": f"Inscrito exitosamente al grupo '{grupo.nombre}'."}