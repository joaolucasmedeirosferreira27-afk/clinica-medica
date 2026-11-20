
import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.usuario import Usuario


# Chave secreta para assinatura dos tokens JWT
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHAVE-APENAS-PARA-DESENVOLVIMENTO-LOCAL"
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Hash seguro de senhas usando Argon2
password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)


def criar_token(dados: dict) -> str:
    payload = dados.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expiracao})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar suas credenciais.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise erro

    except jwt.InvalidTokenError:
        raise erro

    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id)
    ).first()

    if not usuario or not usuario.ativo:
        raise erro

    return usuario


def exigir_perfis(*perfis_permitidos):
    def verificar_permissao(
        usuario: Usuario = Depends(get_usuario_atual)
    ):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não possui permissão para acessar este recurso."
            )

        return usuario

    return verificar_permissao
