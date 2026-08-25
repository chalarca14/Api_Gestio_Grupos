from fastapi import FastAPI
from app.database import engine, Base
import app.models  # Carga de modelos para creación de tablas

from app.routers import (
    auth,
    usuarios,
    estudiantes,
    instructores,
    grupos,
    trabajos,
    entregas,
    calificaciones,
    asistencias,
    notificaciones,
)

# Crear tablas en SQLite si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestión de Grupos Académicos")

# Ruta de inicio / bienvenida
@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "¡La API de Gestión de Grupos está funcionando correctamente!",
        "estado": "activa",
        "documentacion": "/docs"
    }

# Inclusión de routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(estudiantes.router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(instructores.router, prefix="/instructores", tags=["Instructores"])
app.include_router(grupos.router, prefix="/grupos", tags=["Grupos"])
app.include_router(trabajos.router, prefix="/trabajos", tags=["Trabajos"])
app.include_router(entregas.router, prefix="/entregas", tags=["Entregas"])
app.include_router(calificaciones.router, prefix="/calificaciones", tags=["Calificaciones"])
app.include_router(asistencias.router, prefix="/asistencias", tags=["Asistencias"])
app.include_router(notificaciones.router, prefix="/notificaciones", tags=["Notificaciones"])