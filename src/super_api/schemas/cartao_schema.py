from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr
from pydantic.v1 import validator


class CartaoResponse(BaseModel):
    id: int
    nome_titular: str = Field(alias="nomeTitular")
    bandeira: Optional[str]
    numero: str
    mes_vencimento: int = Field(alias="mesVencimento")
    ano_vencimento: int = Field(alias="anoVencimento")

    class Config:
        populate_by_name = True
        validate_by_name = True
        from_attributes = True

class CartaoCadastro(BaseModel):
    numero: constr(min_length=12, max_length=30)
    nome_titular: constr(min_length=2, max_length=120) = Field(alias="nomeTitular")
    mes_vencimento: int = Field(..., ge=1, le=12, alias="mesVencimento")
    ano_vencimento: int = Field(..., ge=2000, alias="anoVencimento")
    cvv: Optional[constr(min_length=3, max_length=4)] = None

    class Config:
        populate_by_name = True
        validate_by_name = True
        from_attributes = True

    @validator("numero")
    def apenas_digitos_espacos(cls, v):
        filtered = ''.join(ch for ch in v if ch.isdigit())
        if not filtered.isdigit():
            raise ValueError("Número do cartão inválido")
        return v

    @validator("ano_vencimento")
    def ano_minimo(cls, v):
        if v < datetime.utcnow().year:
            raise ValueError("Ano de expiração inválido")
        return v

    @validator("cvv")
    def cvv_digitos(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError("CVV deve conter apenas dígitos")
        return v

