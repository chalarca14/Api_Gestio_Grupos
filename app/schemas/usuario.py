from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str

class UsuarioCrear(UsuarioBase):
    password: str

class UsuarioRespuesta(UsuarioBase):
    id: int

    class Config:
        from_attributes = True