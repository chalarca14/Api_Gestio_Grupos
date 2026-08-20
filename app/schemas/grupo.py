from pydantic import BaseModel, ConfigDict

class GrupoBase(BaseModel):
    nombre: str

class GrupoCrear(GrupoBase):
    pass

class UnirseGrupo(BaseModel):
    codigo: str

class GrupoRespuesta(GrupoBase):
    id: int
    codigo: str
    instructor_id: int

    model_config = ConfigDict(from_attributes=True)