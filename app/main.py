from fastapi import FastAPI
from app.database import engine, Base
from app.routers import usuarios, grupos, trabajos, auth

import app.models.usuario
import app.models.grupo
import app.models.grupo_estudiante
import app.models.trabajo


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Gestión de Grupos y Entregas Académicas",
    description="API para gestionar grupos, trabajos y entregas académicas.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(grupos.router)
app.include_router(trabajos.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Gestión de Grupos funcionando correctamente"
    }
