
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Endereço do banco de dados
DATABASE_URL = "sqlite:///./backend/clinica.db"

# Configuração da conexão
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Gerenciamento das sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Classe base para os modelos
class Base(DeclarativeBase):
    pass


# Dependência para disponibilizar sessões
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
