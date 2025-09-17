import importlib
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Header
from dotenv import load_dotenv
import os

jwt = importlib.import_module("jwt")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criptografar_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha, hash_senha)

def gerar_token(usuario_id: int, email: str):
    try:
        payload = {
            "sub": str(usuario_id),
            "email": email,
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
        return payload.get("sub")  # get evita KeyError
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
