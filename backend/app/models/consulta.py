
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from backend.app.database import Base


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)

    paciente_id = Column(
        Integer,
        ForeignKey("pacientes.id"),
        nullable=False
    )

    medico_id = Column(
        Integer,
        ForeignKey("medicos.id"),
        nullable=False
    )

    data_hora = Column(DateTime, nullable=False, index=True)

    status = Column(
        String(20),
        nullable=False,
        default="agendada"
    )

    observacoes = Column(String(500), nullable=True)

    criado_em = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
