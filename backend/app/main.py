
from fastapi import FastAPI

from backend.app.database import engine, Base
from backend.app import models
from backend.app.routers import auth, pacientes, medicos, consultas
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Sistema de Gestão para Clínica Médica",
    description="API para gerenciamento de uma clínica médica.",
    version="1.0.0"
    
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)


# Rotas de autenticação
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)


# Rotas de pacientes
app.include_router(
    pacientes.router,
    prefix="/pacientes",
    tags=["Pacientes"]
)


# Rotas de médicos e especialidades
app.include_router(
    medicos.router,
    prefix="/medicos",
    tags=["Médicos e Especialidades"]
)


# Rotas de consultas
app.include_router(
    consultas.router,
    prefix="/consultas",
    tags=["Consultas"]
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

@app.get("/app", response_class=HTMLResponse)
def abrir_sistema():
    arquivo = BASE_DIR / "templates" / "index.html"
    return arquivo.read_text(encoding="utf-8")