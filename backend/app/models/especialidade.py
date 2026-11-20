
from sqlalchemy import Column, Integer, String
from backend.app.database import Base


class Especialidade(Base):

    __tablename__ = "especialidades"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(100), unique=True, nullable=False)

    descricao = Column(String(255))
