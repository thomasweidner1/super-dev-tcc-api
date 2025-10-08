from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.super_api.auth.auth import gerar_token, criptografar_senha, verificar_token, get_current_user
from src.super_api.auth.usuario_service import login_usuario
from src.super_api.database.modelos import UsuarioEntidade, EnderecoEntidade, CartaoEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.endereco_schema import Endereco
from src.super_api.schemas.user_schema import UsuarioCadastro, Usuario, UsuarioEditar, UsuarioResponse

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
            telefone=form.telefone,
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
            complemento=form.endereco.complemento,
            cep=form.endereco.cep,
            usuario_id=usuario.id,
            bairro=form.endereco.bairro,
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

        return {
            "token": token,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Obter dados do usuário
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
        cep=endereco_entidade.cep,
        complemento=endereco_entidade.complemento,
        bairro=endereco_entidade.bairro,
    ) if endereco_entidade else None

    usuario = Usuario(
        id=usuario_db.id,
        nomeCompleto=usuario_db.nome_completo,
        dataNascimento=usuario_db.data_nascimento,
        cpf=usuario_db.cpf,
        email=usuario_db.email,
        senha=usuario_db.senha,
        telefone=usuario_db.telefone,
        nivel=usuario_db.nivel,
        foto_url=usuario_db.foto_url,
        idioma=usuario_db.idioma,
        tema=usuario_db.tema,
        notificacoes=usuario_db.notificacoes,
        endereco=endereco
    )
    return usuario

# Editar dados do usuário na tela de perfil
@router.patch("/me", response_model=UsuarioResponse)
def atualizar_usuario(
    form: UsuarioEditar,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    usuario = db.query(UsuarioEntidade).filter_by(id=usuario_atual.id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    dados = form.dict(exclude_unset=True)

    for campo, valor in dados.items():
        if campo != "endereco":
            setattr(usuario, campo, valor)

    if "endereco" in dados and dados["endereco"] is not None:
        for campo, valor in dados["endereco"].items():
            setattr(usuario.enderecos[0], campo, valor)

    db.commit()
    db.refresh(usuario)
    return UsuarioResponse(
        id=usuario.id,
        nome_completo=usuario.nome_completo,
        email=usuario.email,
        nivel=usuario.nivel
    )