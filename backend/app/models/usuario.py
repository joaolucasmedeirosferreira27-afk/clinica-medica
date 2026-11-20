
from sqlalchemy import Column, Integer, String, Boolean
from backend.app.database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    senha_hash = Column(String(255), nullable=False)

    perfil = Column(String(20), nullable=False)

    ativo = Column(Boolean, default=True)
