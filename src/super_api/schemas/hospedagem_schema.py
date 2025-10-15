from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Hospedagem(BaseModel):
    nome: str
    descricao: str
    preco_noite: float = Field(alias="precoNoite")
    capacidade: int
    tipo: str
    ativo: bool = True

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class HospedagemCadastro(Hospedagem):
    usuario_id: int = Field(..., alias="usuarioId")
    endereco_id: int = Field(..., alias="enderecoId")
    imagens: Optional[List[str]] = []
    comodidades: Optional[List[str]] = []

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class HospedagemEditar(Hospedagem):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco_noite: Optional[float] = Field(None, alias="precoNoite")
    capacidade: Optional[int] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None
    imagens: Optional[List[str]] = None
    comodidades: Optional[List[str]] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class ImagemOut(BaseModel):
    id: int
    url: str

    class Config:
        orm_mode = True


class ComodidadeOut(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class HospedagemResponse(Hospedagem):
    id: int
    usuario_id: int = Field(..., alias="usuarioId")
    endereco_id: int = Field(..., alias="enderecoId")
    imagens: List[ImagemOut] = []
    comodidades: List[ComodidadeOut] = []
    criado_em: Optional[datetime] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True
