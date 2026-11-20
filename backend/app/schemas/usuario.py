
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


PerfilUsuario = Literal[
    "administrador",
    "medico",
    "recepcao",
    "paciente"
]


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    email: str = Field(min_length=5, max_length=150)
    senha: str = Field(min_length=8, max_length=128)
    perfil: PerfilUsuario


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BootstrapAdmin(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    email: str = Field(min_length=5, max_length=150)
    senha: str = Field(min_length=8, max_length=128)