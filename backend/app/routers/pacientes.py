
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.paciente import Paciente
from backend.app.schemas.paciente import (
    PacienteCreate,
    PacienteUpdate,
    PacienteResponse
)
from backend.app.models.usuario import Usuario
from backend.app.security.auth import exigir_perfis


router = APIRouter()


@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_paciente(
    dados: PacienteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis("administrador", "recepcao")
    )
):
    paciente_existente = db.query(Paciente).filter(
        Paciente.cpf == dados.cpf
    ).first()

    if paciente_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um paciente cadastrado com esse CPF."
        )

    novo_paciente = Paciente(**dados.model_dump())

    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)

    return novo_paciente


@router.get(
    "/",
    response_model=list[PacienteResponse]
)
def listar_pacientes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    return db.query(Paciente).order_by(Paciente.nome).all()


@router.get(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def consultar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis("administrador", "recepcao", "medico")
    )
):
    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado."
        )

    return paciente


@router.put(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def atualizar_paciente(
    paciente_id: int,
    dados: PacienteUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis("administrador", "recepcao")
    )
):
    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado."
        )

    atualizacoes = dados.model_dump(exclude_unset=True)

    novo_cpf = atualizacoes.get("cpf")

    if novo_cpf and novo_cpf != paciente.cpf:
        cpf_existente = db.query(Paciente).filter(
            Paciente.cpf == novo_cpf
        ).first()

        if cpf_existente:
            raise HTTPException(
                status_code=400,
                detail="Esse CPF já está cadastrado."
            )

    for campo, valor in atualizacoes.items():
        setattr(paciente, campo, valor)

    db.commit()
    db.refresh(paciente)

    return paciente
