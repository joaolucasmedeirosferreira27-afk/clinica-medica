
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConsultaCreate(BaseModel):
    paciente_id: int = Field(gt=0)
    medico_id: int = Field(gt=0)
    data_hora: datetime
    observacoes: str | None = Field(default=None, max_length=500)

    @field_validator("data_hora")
    @classmethod
    def validar_data_hora(cls, valor):
        if valor.tzinfo is not None:
            raise ValueError("Informe a data e hora local sem fuso horário.")
        return valor


class ConsultaUpdate(BaseModel):
    data_hora: datetime | None = None
    observacoes: str | None = Field(default=None, max_length=500)

    @field_validator("data_hora")
    @classmethod
    def validar_data_hora(cls, valor):
        if valor is not None and valor.tzinfo is not None:
            raise ValueError("Informe a data e hora local sem fuso horário.")
        return valor


class ConsultaStatusUpdate(BaseModel):
    status: Literal["agendada", "cancelada", "realizada"]


class ConsultaResponse(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: str
    observacoes: str | None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)
