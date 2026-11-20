
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.consulta import Consulta
from backend.app.models.paciente import Paciente
from backend.app.models.medico import Medico
from backend.app.schemas.consulta import (
    ConsultaCreate,
    ConsultaUpdate,
    ConsultaStatusUpdate,
    ConsultaResponse
)
from backend.app.security.auth import exigir_perfis


router = APIRouter()

PERFIS_GESTAO = ("administrador", "recepcao")


def validar_agendamento(db, medico_id, data_hora, consulta_id=None):
    if data_hora <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar consultas no passado."
        )

    conflito = db.query(Consulta).filter(
        Consulta.medico_id == medico_id,
        Consulta.data_hora == data_hora,
        Consulta.status == "agendada"
    )

    if consulta_id is not None:
        conflito = conflito.filter(Consulta.id != consulta_id)

    if conflito.first():
        raise HTTPException(
            status_code=409,
            detail="O médico já possui consulta nesse horário."
        )


@router.post("/", response_model=ConsultaResponse, status_code=201)
def agendar_consulta(
    dados: ConsultaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(*PERFIS_GESTAO))
):
    if not db.get(Paciente, dados.paciente_id):
        raise HTTPException(404, "Paciente não encontrado.")

    if not db.get(Medico, dados.medico_id):
        raise HTTPException(404, "Médico não encontrado.")

    validar_agendamento(
        db, dados.medico_id, dados.data_hora
    )

    consulta = Consulta(**dados.model_dump())

    db.add(consulta)
    db.commit()
    db.refresh(consulta)

    return consulta


@router.get("/", response_model=list[ConsultaResponse])
def listar_consultas(
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    return db.query(Consulta).order_by(
        Consulta.data_hora
    ).all()


@router.get("/{consulta_id}", response_model=ConsultaResponse)
def consultar_consulta(
    consulta_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    consulta = db.get(Consulta, consulta_id)

    if not consulta:
        raise HTTPException(404, "Consulta não encontrada.")

    return consulta


@router.put("/{consulta_id}", response_model=ConsultaResponse)
def reagendar_consulta(
    consulta_id: int,
    dados: ConsultaUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(*PERFIS_GESTAO))
):
    consulta = db.get(Consulta, consulta_id)

    if not consulta:
        raise HTTPException(404, "Consulta não encontrada.")

    if consulta.status != "agendada":
        raise HTTPException(
            400,
            "Somente consultas agendadas podem ser alteradas."
        )

    atualizacoes = dados.model_dump(exclude_unset=True)

    if "data_hora" in atualizacoes:
        if atualizacoes["data_hora"] is None:
            raise HTTPException(400, "Data e hora são obrigatórias.")

        validar_agendamento(
            db,
            consulta.medico_id,
            atualizacoes["data_hora"],
            consulta.id
        )

    for campo, valor in atualizacoes.items():
        setattr(consulta, campo, valor)

    db.commit()
    db.refresh(consulta)

    return consulta


@router.patch(
    "/{consulta_id}/status",
    response_model=ConsultaResponse
)
def alterar_status(
    consulta_id: int,
    dados: ConsultaStatusUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(*PERFIS_GESTAO))
):
    consulta = db.get(Consulta, consulta_id)

    if not consulta:
        raise HTTPException(404, "Consulta não encontrada.")

    if consulta.status != "agendada":
        raise HTTPException(
            400,
            "Não é possível alterar uma consulta já finalizada."
        )

    if dados.status == "agendada":
        raise HTTPException(
            400,
            "A consulta já está agendada."
        )

    consulta.status = dados.status

    db.commit()
    db.refresh(consulta)

    return consulta
