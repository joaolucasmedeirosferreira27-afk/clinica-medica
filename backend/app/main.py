
from fastapi import FastAPI

from backend.app.database import engine, Base
from backend.app import models
from backend.app.routers import auth


app = FastAPI(
    title="Sistema de Gestão para Clínica Médica",
    description="API para gerenciamento de uma clínica médica.",
    version="1.0.0"
)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Registro das rotas
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
     pacientes.router,
    prefix="/pacientes",
    tags=["Pacientes"]
)


@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Clínica Médica funcionando!",
        "status": "online"
    }


@app.get("/health")
def verificar_saude():
    return {"status": "healthy"}


@app.get("/health/database")
def verificar_banco():
    return {"database": "connected"}

from backend.app.routers import pacientes