from pydantic import BaseModel, ConfigDict, Field


class EspecialidadeCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    descricao: str | None = None


class EspecialidadeResponse(EspecialidadeCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MedicoCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=150)
    crm: str = Field(min_length=4, max_length=30)
    telefone: str | None = None
    email: str | None = None
    especialidade_id: int


class MedicoResponse(MedicoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)