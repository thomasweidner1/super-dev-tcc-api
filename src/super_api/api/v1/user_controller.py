from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.super_api.auth.auth import gerar_token, criptografar_senha, verificar_token
from src.super_api.auth.usuario_service import login_usuario, cadastrar_usuario
from src.super_api.database.modelos import UsuarioEntidade, EnderecoEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.endereco_schema import Endereco
from src.super_api.schemas.user_schema import UsuarioCadastro, Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/me")
def obter_dados(user_id: int = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioEntidade).filter(UsuarioEntidade.id == user_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    endereco_entidade = usuario_db.enderecos[0] if usuario_db.enderecos else None

    endereco = Endereco(
        rua=endereco_entidade.rua,
        numero=endereco_entidade.numero,
        cidade=endereco_entidade.cidade,
        estado=endereco_entidade.estado,
        # cep=endereco_entidade.cep,
    ) if endereco_entidade else None

    usuario = Usuario(
        id=usuario_db.id,
        nomeCompleto=usuario_db.nome_completo,  # usando alias
        dataNascimento=usuario_db.data_nascimento,
        cpf=usuario_db.cpf,
        email=usuario_db.email,
        senha=usuario_db.senha,
        nivel=usuario_db.nivel,
        endereco=endereco
    )
    return usuario


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
            senha=hash_senha
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        token = gerar_token(usuario.id, usuario.email)

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

