from typing import Optional
from pydantic import BaseModel


class Endereco(BaseModel):
    rua: str
    numero: str
    cidade: str
    estado: str
    cep: str
    bairro: str
    complemento: str

    class Config:
        from_attributes = True


class EnderecoEditar(BaseModel):
    rua: Optional[str]
    numero: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    complemento: Optional[str]

    class Config:
        from_attributes = True

