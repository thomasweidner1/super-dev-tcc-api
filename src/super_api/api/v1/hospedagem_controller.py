from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.super_api.database.modelos import HospedagemEntidade, ImagemHospedagemEntidade, ComodidadeEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.hospedagem_schema import HospedagemCadastro, HospedagemResponse

router = APIRouter(prefix="/hospedagem", tags=["Hospedagem"])

@router.post("/cadastrar", response_model=HospedagemResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_hospedagem(form: HospedagemCadastro, db: Session = Depends(get_db)):
    try:
        nova_hospedagem = HospedagemEntidade(
            nome=form.nome,
            descricao=form.descricao,
            preco_noite=form.preco_noite,
            capacidade=form.capacidade,
            tipo=form.tipo,
            ativo=form.ativo,
            usuario_id=form.usuario_id,
            endereco_id=form.endereco_id,
        )

        db.add(nova_hospedagem)
        db.commit()
        db.refresh(nova_hospedagem)

        if form.imagens:
            for url in form.imagens:
                imagem = ImagemHospedagemEntidade(
                    url=url, hospedagem_id=nova_hospedagem.id
                )
                db.add(imagem)

        if form.comodidades:
            for nome in form.comodidades:
                comodidade = ComodidadeEntidade(
                    nome=nome, hospedagem_id=nova_hospedagem.id
                )
                db.add(comodidade)

        db.commit()
        db.refresh(nova_hospedagem)

        return nova_hospedagem

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao cadastrar hospedagem: {str(e)}",
        )

