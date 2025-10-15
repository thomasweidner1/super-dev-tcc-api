import importlib
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Header
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.super_api.database.modelos import UsuarioEntidade
from src.super_api.dependencias import get_db

jwt = importlib.import_module("jwt")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha, hash_senha)

def gerar_token(usuario_id: int, email: str, nivel: str):
    try:
        payload = {
            "sub": str(usuario_id),
            "email": email,
            "nivel": nivel,
            "exp": datetime.now(timezone.utc) + timedelta(hours=12)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar token: {str(e)}")

def verificar_token(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")

    token = Authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user(user_id: int = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario = db.query(UsuarioEntidade).filter(UsuarioEntidade.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario