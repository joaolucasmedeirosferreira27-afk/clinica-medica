
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.usuario import Usuario
from backend.app.schemas.usuario import (
    BootstrapAdmin,
    UsuarioResponse,
    LoginResponse
)
from backend.app.security.auth import (
    hash_senha,
    verificar_senha,
    criar_token,
    get_usuario_atual,
    exigir_perfis
)


router = APIRouter()


# Inicialização do primeiro administrador
@router.post(
    "/bootstrap-admin",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_administrador_inicial(
    dados: BootstrapAdmin,
    db: Session = Depends(get_db)
):
    if db.query(Usuario).count() > 0:
        raise HTTPException(
            status_code=403,
            detail="A inicialização já foi realizada."
        )

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email.lower().strip(),
        senha_hash=hash_senha(dados.senha),
        perfil="administrador",
        ativo=True
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# Login
@router.post("/login", response_model=LoginResponse)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = formulario.username.lower().strip()

    usuario = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if (
        not usuario
        or not verificar_senha(
            formulario.password,
            usuario.senha_hash
        )
        or not usuario.ativo
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    token = criar_token({
        "sub": str(usuario.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Consultar usuário autenticado
@router.get("/me", response_model=UsuarioResponse)
def consultar_usuario_atual(
    usuario: Usuario = Depends(get_usuario_atual)
):
    return usuario


# Rota de demonstração da autorização administrativa
@router.get("/admin-check")
def verificar_acesso_administrador(
    usuario: Usuario = Depends(
        exigir_perfis("administrador")
    )
):
    return {
        "mensagem": "Acesso administrativo autorizado.",
        "usuario": usuario.nome
    }
