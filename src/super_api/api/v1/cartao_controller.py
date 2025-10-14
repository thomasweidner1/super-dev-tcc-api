from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.super_api.auth.auth import verificar_token, get_current_user
from src.super_api.database.modelos import CartaoEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.cartao_schema import CartaoResponse, CartaoCadastro

router = APIRouter(prefix="/usuarios/cartoes", tags=["Cartoes"])


def validacao(numero: str) -> bool:
    numero = ''.join(filter(str, numero))
    def digitos_de(n):
        return [int(d) for d in n]
    digitos = digitos_de(numero)
    soma_impar = sum(digitos[-1::-2])
    soma_par = 0
    for d in digitos[-2::-2]:
        duplicado = d * 2
        soma_par += duplicado if duplicado < 10 else duplicado - 9
    return (soma_impar + soma_par) % 10 == 0

def definir_bandeira(numero: str) -> str:
    n = numero.replace(" ", "")
    if n.startswith(("4",)):
        return "Visa"
    if n[:2] in ("51","52","53","54","55") or (len(n) >= 4 and 2221 <= int(n[:4]) <= 2720):
        return "Mastercard"
    if n.startswith(("34","37")):
        return "American Express"
    if n.startswith("6"):
        return "Discover"
    return "Desconhecido"


def mascarar_numero(numero: str) -> str:
    digitos = ''.join(ch for ch in numero if ch.isdigit())
    if len(digitos) <= 4:
        return '*' * len(digitos)
    mascara = '*' * (len(digitos) - 4) + digitos[-4:]
    formatado = ' '.join(mascara[i:i + 4] for i in range(0, len(mascara), 4))
    return formatado


@router.post("/cadastrar", response_model=CartaoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_cartao(
    cartao: CartaoCadastro,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    # 1) Validação
    digitos = ''.join(filter(str, cartao.numero))
 #   if not validacao(digitos):
 #       raise HTTPException(status_code=400, detail="Número de cartão inválido.")

    # 2) Valida expiracao (mês/ano no futuro)
    agora = datetime.utcnow()
    ano_vencimento = cartao.ano_vencimento
    mes_vencimento = cartao.mes_vencimento
    if ano_vencimento < agora.year or (ano_vencimento == agora.year and mes_vencimento < agora.month):
        raise HTTPException(status_code=400, detail="Cartão expirado.")

    # 3) Detecta bandeira e prepara campos a salvar
    bandeira = definir_bandeira(digitos)
    formatado = mascarar_numero(digitos)

    if cartao.cvv:
        pass

    # 4) Persistir CartaoEntidade (salvando apenas masked + last4)
    novo_cartao = CartaoEntidade(
        usuario_id=usuario_atual.id,
        nome_titular=cartao.nome_titular,
        bandeira=bandeira,
        numero=formatado,
        mes_vencimento=mes_vencimento,
        ano_vencimento=ano_vencimento
    )
    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)

    return novo_cartao


@router.get("/meus-cartoes", response_model=list[CartaoResponse])
def listar_cartoes(db: Session = Depends(get_db),usuario_atual=Depends(get_current_user)):
    cartoes = db.query(CartaoEntidade).filter_by(usuario_id=usuario_atual.id).all()
    if cartoes:
        return cartoes
    raise HTTPException(status_code=404, detail="Nenhum cartão encontrado")

@router.delete("/apagar/{cartao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cartao(cartao_id: int, db: Session = Depends(get_db), usuario_atual=Depends(get_current_user)):

    cartao = db.query(CartaoEntidade).filter_by(id=cartao_id).first()
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")

    if cartao.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este cartão")

    db.delete(cartao)
    db.commit()
    return