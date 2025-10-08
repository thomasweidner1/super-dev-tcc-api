from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.super_api.auth.auth import gerar_token, criptografar_senha, verificar_token, get_current_user
from src.super_api.auth.usuario_service import login_usuario
from src.super_api.database.modelos import UsuarioEntidade, EnderecoEntidade, CartaoEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.cartao_schema import CartaoResponse, CartaoCadastro
from src.super_api.schemas.endereco_schema import Endereco
from src.super_api.schemas.user_schema import UsuarioCadastro, Usuario, UsuarioEditar, UsuarioResponse

router = APIRouter(prefix="/usuarios/cartoes", tags=["Cartoes"])


def mascarar_numero(numero: str) -> str:
    return f"**** **** **** {numero[-4:]}"

@router.post("/cadastrar", response_model=CartaoResponse)
def cadastrar_cartao(cartao: CartaoCadastro, user=Depends(verificar_token), db: Session = Depends(get_db)
):
    user_id = user if isinstance(user, int) else getattr(user, "id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")


    cartao_existente = db.query(CartaoEntidade).filter(
        CartaoEntidade.numero == cartao.numero,
        CartaoEntidade.usuario_id == user_id
    ).first()
    if cartao_existente:
        raise HTTPException(status_code=400, detail="Cartão já cadastrado para este usuário")

    novo_cartao = CartaoEntidade(
        numero=cartao.numero,
        nome_titular=cartao.nome_titular,
        validade=cartao.validade,
        cvv=cartao.cvv,
        cpf_titular=cartao.cpf_titular,
        usuario_id=user_id
    )

    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)


@router.get("/meus-cartoes", response_model=List[CartaoResponse])
def obter_cartoes(user=Depends(verificar_token)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return user.cartoes