
from sqlalchemy import Column, Integer, String, Date, Text
from backend.app.database import Base


class Paciente(Base):

    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    cpf = Column(String(14), unique=True, nullable=False)

    data_nascimento = Column(Date, nullable=False)

    telefone = Column(String(20))

    email = Column(String(150))

    endereco = Column(String(255))

    historico_medico = Column(Text)

    alergias = Column(Text)
