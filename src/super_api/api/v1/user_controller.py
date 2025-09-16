from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.super_api.auth.auth import gerar_token, criptografar_senha
from src.super_api.auth.usuario_service import login_usuario, cadastrar_usuario
from src.super_api.database.modelos import UsuarioEntidade, EnderecoEntidade
from src.super_api.dependencias import get_db
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
def cadastro_usuario(form: UsuarioCadastro, db: Session = Depends(get_db)):
    try:
        if db.query(UsuarioEntidade).filter_by(email=form.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        if db.query(UsuarioEntidade).filter_by(cpf=form.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        hash_senha = criptografar_senha(form.senha)

        usuario = UsuarioEntidade(
            nome_completo=form.nome_completo,
            data_nascimento=form.data_nascimento,
            cpf=form.cpf,
            email=form.email,
            senha=hash_senha,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        token = gerar_token(usuario.id)

        endereco = EnderecoEntidade(
            rua=form.endereco.rua,
            numero=form.endereco.numero,
            cidade=form.endereco.cidade,
            estado=form.endereco.estado,
            usuario_id=usuario.id
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

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
            "token": token,
        }

    except Exception as e:
        import traceback
        traceback.print_exc()  # mostra o erro completo no console
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

