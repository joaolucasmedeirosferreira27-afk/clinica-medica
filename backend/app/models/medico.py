
from sqlalchemy import Column, Integer, String, ForeignKey
from backend.app.database import Base


class Medico(Base):

    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    crm = Column(String(30), unique=True, nullable=False)

    telefone = Column(String(20))

    email = Column(String(150))

    especialidade_id = Column(
        Integer,
        ForeignKey("especialidades.id"),
        nullable=False
    )
