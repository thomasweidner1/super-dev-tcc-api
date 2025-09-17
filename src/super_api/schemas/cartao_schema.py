from datetime import datetime
from pydantic import BaseModel, Field


class Cartao(BaseModel):
    id: int
    numero: str = Field(alias="cartaoNumero")
    nome_titular: str = Field(alias="cartaoNome")
    cpf_titular: str = Field(alias="cartaoCPF")
    cvv: str = Field(alias="cartaoCVV")
    validade: datetime = Field(alias="cartaoValidade")

class CartaoCadastro(BaseModel):
    numero: str = Field(alias="cartaoNumero")
    nome_titular: str = Field(alias="cartaoNome")
    cpf_titular: str = Field(alias="cartaoCPF")
    cvv: str = Field(alias="cartaoCVV")
    validade: datetime = Field(alias="cartaoValidade")