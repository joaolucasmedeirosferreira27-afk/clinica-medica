
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PacienteCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    cpf: str = Field(min_length=11, max_length=14)
    data_nascimento: date
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    historico_medico: str | None = None
    alergias: str | None = None


class PacienteUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=150)
    cpf: str | None = Field(default=None, min_length=11, max_length=14)
    data_nascimento: date | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    historico_medico: str | None = None
    alergias: str | None = None


class PacienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str | None
    email: str | None
    endereco: str | None
    historico_medico: str | None
    alergias: str | None

    model_config = ConfigDict(from_attributes=True)
