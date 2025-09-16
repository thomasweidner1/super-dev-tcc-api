from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.super_api.auth.usuario_service import login_usuario, cadastrar_usuario
from src.super_api.database.modelos import UsuarioEntidade
from src.super_api.dependencias import get_db
from src.super_api.auth.auth import gerar_token, criptografar_senha
from src.super_api.schemas.user_schema import UsuarioCadastro

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/login")
def login_endpoint(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    senha = data.get("senha")

    resultado = login_usuario(db, email, senha)
    if not resultado:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    return resultado

@router.post("/cadastro")
def cadastro_endpoint(form: UsuarioCadastro, db: Session = Depends(get_db)):
    if db.query(UsuarioEntidade).filter_by(email=form.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(UsuarioEntidade).filter_by(cpf=form.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    usuario, endereco, token = cadastrar_usuario(db, form)

    return {
        "mensagem": "Usuário cadastrado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome_completo": usuario.nome_completo,
            "email": usuario.email,
            "nivel": usuario.nivel
        },
        "endereco": {
            "rua": endereco.rua,
            "numero": endereco.numero,
            "cidade": endereco.cidade,
            "estado": endereco.estado,
            "complemento": endereco.complemento
        },
        "token": token
    }
