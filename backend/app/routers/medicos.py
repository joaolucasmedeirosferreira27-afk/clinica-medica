from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.medico import Medico
from backend.app.models.especialidade import Especialidade
from backend.app.schemas.medico import (
    EspecialidadeCreate,
    EspecialidadeResponse,
    MedicoCreate,
    MedicoResponse
)
from backend.app.security.auth import exigir_perfis

router = APIRouter()


@router.post(
    "/especialidades",
    response_model=EspecialidadeResponse,
    status_code=201
)
def cadastrar_especialidade(
    dados: EspecialidadeCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis("administrador"))
):
    existente = db.query(Especialidade).filter(
        Especialidade.nome == dados.nome
    ).first()

    if existente:
        raise HTTPException(400, "Especialidade já cadastrada.")

    especialidade = Especialidade(**dados.model_dump())
    db.add(especialidade)
    db.commit()
    db.refresh(especialidade)

    return especialidade


@router.get(
    "/especialidades",
    response_model=list[EspecialidadeResponse]
)
def listar_especialidades(
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    return db.query(Especialidade).order_by(
        Especialidade.nome
    ).all()


@router.post(
    "/",
    response_model=MedicoResponse,
    status_code=201
)
def cadastrar_medico(
    dados: MedicoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis("administrador"))
):
    especialidade = db.get(
        Especialidade, dados.especialidade_id
    )

    if not especialidade:
        raise HTTPException(404, "Especialidade não encontrada.")

    existente = db.query(Medico).filter(
        Medico.crm == dados.crm
    ).first()

    if existente:
        raise HTTPException(400, "CRM já cadastrado.")

    medico = Medico(**dados.model_dump())

    db.add(medico)
    db.commit()
    db.refresh(medico)

    return medico


@router.get("/", response_model=list[MedicoResponse])
def listar_medicos(
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    return db.query(Medico).order_by(Medico.nome).all()


@router.get("/{medico_id}", response_model=MedicoResponse)
def consultar_medico(
    medico_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    medico = db.get(Medico, medico_id)

    if not medico:
        raise HTTPException(404, "Médico não encontrado.")

    return medico