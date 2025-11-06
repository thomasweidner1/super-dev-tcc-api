from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.super_api.auth.auth import get_current_user
from src.super_api.database.modelos import HospedagemEntidade, ImagemHospedagemEntidade, ComodidadeEntidade, \
    EnderecoEntidade
from src.super_api.dependencias import get_db
from src.super_api.schemas.hospedagem_schema import HospedagemCadastro, HospedagemResponse

router = APIRouter(prefix="/hospedagem", tags=["Hospedagem"])

@router.post("/cadastrar", response_model=HospedagemResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_hospedagem(form: HospedagemCadastro, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    if usuario.nivel not in ['host_standard', 'host_plus', 'host_premium']:
        raise HTTPException(status_code=401, detail="Usuário não tem permissão")

    limites = {
        'host_standard': 1,
        'host_plus': 3,
        'host_premium': float('inf')
    }

    qtd_hosp = db.query(HospedagemEntidade).filter(HospedagemEntidade.usuario_id == usuario.id).count()
    limite = limites.get(usuario.nivel)

    if qtd_hosp >= limite:
        raise HTTPException(
            status_code=403,
            detail=f"Limite de hospedagens atingido para o plano {usuario.nivel}."
        )

    try:
        novo_endereco = EnderecoEntidade(
            estado=form.endereco.estado,
            cidade=form.endereco.cidade,
            rua=form.endereco.rua,
            numero=form.endereco.numero,
            bairro=form.endereco.bairro,
            complemento=form.endereco.complemento,
            cep=form.endereco.cep,
            usuario_id=usuario.id
        )
        db.add(novo_endereco)
        db.flush()

        nova_hospedagem = HospedagemEntidade(
            nome=form.nome,
            descricao=form.descricao,
            preco_noite=form.preco_noite,
            capacidade=form.capacidade,
            tipo=form.tipo,
            ativo=form.ativo,
            usuario_id=usuario.id,
            endereco_id=novo_endereco.id
        )

        db.add(nova_hospedagem)
        db.flush()

        if form.imagens:
            for url in form.imagens:
                db.add(ImagemHospedagemEntidade(url=url, hospedagem_id=nova_hospedagem.id))

        if form.comodidades:
            for nome in form.comodidades:
                db.add(ComodidadeEntidade(nome=nome, hospedagem_id=nova_hospedagem.id))

        db.commit()
        db.refresh(nova_hospedagem)
        return nova_hospedagem

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar hospedagem: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao cadastrar hospedagem: {str(e)}",
        )


@router.get("/listar")
def listar_hospedagens(
    db: Session = Depends(get_db),
    cidade: str | None = None,
    tipo: str | None = None,
    preco_min: float | None = None,
    preco_max: float | None = None,
    capacidade_min: int | None = None,
):
    query = db.query(HospedagemEntidade)

    if cidade:
        query = query.join(HospedagemEntidade.endereco).filter(HospedagemEntidade.endereco.has(cidade=cidade))
    if tipo:
        query = query.filter(HospedagemEntidade.tipo == tipo)
    if preco_min is not None:
        query = query.filter(HospedagemEntidade.preco_noite >= preco_min)
    if preco_max is not None:
        query = query.filter(HospedagemEntidade.preco_noite <= preco_max)
    if capacidade_min is not None:
        query = query.filter(HospedagemEntidade.capacidade >= capacidade_min)

    hospedagens = query.all()

    return [
        {
            "id": h.id,
            "nome": h.nome,
            "preco_noite": h.preco_noite,
            "tipo": h.tipo,
            "capacidade": h.capacidade,
            "cidade": h.endereco.cidade if h.endereco else None,
            "fotos": h.imagens if h.imagens else [],
        }
        for h in hospedagens
    ]

@router.get("/listar-resumo")
def listar_hospedagens_resumo(db: Session = Depends(get_db)):
    hospedagens = db.query(
        HospedagemEntidade.id,
        HospedagemEntidade.nome,
        HospedagemEntidade.preco_noite,
        HospedagemEntidade.tipo,
    ).filter(HospedagemEntidade.ativo == True).all()

    return [
        {
            "id": h.id,
            "nome": h.nome,
            "preco_noite": h.preco_noite,
            "tipo": h.tipo,
        }
        for h in hospedagens
    ]

@router.get("/detalhes/{hospedagem_id}")
def hospedagem_detalhes(hospedagem_id: int, db: Session = Depends(get_db)):
    hospedagem = (
        db.query(HospedagemEntidade)
        .filter(HospedagemEntidade.id == hospedagem_id)
        .first()
    )

    if not hospedagem:
        raise HTTPException(status_code=404, detail="Hospedagem não encontrada")

    return {
        "id": hospedagem.id,
        "nome": hospedagem.nome,
        "descricao": hospedagem.descricao,
        "preco_noite": hospedagem.preco_noite,
        "capacidade": hospedagem.capacidade,
        "tipo": hospedagem.tipo,
        "ativo": hospedagem.ativo,
        "usuario_id": hospedagem.usuario_id,
        "endereco": {
            "id": hospedagem.endereco.id,
            "rua": hospedagem.endereco.rua,
            "numero": hospedagem.endereco.numero,
            "cidade": hospedagem.endereco.cidade,
            "estado": hospedagem.endereco.estado,
        } if hospedagem.endereco else None,
        "fotos": [
            {"url": f.url}
            for f in hospedagem.imagens
        ],
    }


@router.get("/minhas")
def listar_minhas_hospedagens(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    hospedagens = db.query(HospedagemEntidade).filter(HospedagemEntidade.usuario_id == usuario.id).all()

    return [
        {
            "id": h.id,
            "nome": h.nome,
            "descricao": h.descricao,
            "preco_noite": h.preco_noite,
            "tipo": h.tipo,
            "capacidade": h.capacidade,
            "ativo": h.ativo,
        }
        for h in hospedagens
    ]
