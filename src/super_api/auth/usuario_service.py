from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.super_api.database.modelos import UsuarioEntidade, EnderecoEntidade
from src.super_api.auth.auth import criptografar_senha, verificar_senha, gerar_token

def login_usuario(db: Session, email: str, senha: str):
    usuario = db.query(UsuarioEntidade).filter_by(email=email).first()
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None

    token = gerar_token(usuario.id)

    return {
        "usuario": {
            "id": usuario.id,
            "nome_completo": usuario.nome_completo,
            "email": usuario.email,
            "nivel": usuario.nivel
        },
        "token": token
    }

def cadastrar_usuario(db: Session, form):
    try:
        # cria usuário
        usuario = UsuarioEntidade(
            nome_completo=form.nome_completo,
            data_nascimento=form.data_nascimento,
            cpf=form.cpf,
            email=form.email,
            senha=criptografar_senha(form.senha),
        )
        db.add(usuario)
        db.flush()  # ainda não confirma no banco

        # gera token
        token = gerar_token(usuario.id)

        # confirma usuário
        db.commit()
        db.refresh(usuario)

        # cria endereço
        endereco = EnderecoEntidade(
            rua=form.endereco.rua,
            numero=form.endereco.numero,
            cidade=form.endereco.cidade,
            estado=form.endereco.estado,
            complemento=form.endereco.complemento,
            usuario_id=usuario.id
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

        return usuario, endereco, token

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar usuário: {str(e)}")
