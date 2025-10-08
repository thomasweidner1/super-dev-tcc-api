from sqlalchemy.orm import Session
from src.super_api.database.modelos import UsuarioEntidade
from src.super_api.auth.auth import verificar_senha, gerar_token


def login_usuario(db: Session, email: str, senha: str):
    usuario = db.query(UsuarioEntidade).filter_by(email=email).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None
    token = gerar_token(usuario.id, usuario.email)

    return {
        "token": token
    }



