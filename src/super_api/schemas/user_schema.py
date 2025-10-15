from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from src.super_api.schemas.endereco_schema import Endereco, EnderecoEditar


class UsuarioResponse(BaseModel):
    id: int
    nome_completo: str
    email: str
    nivel: str



class Usuario(BaseModel):
    id: int | None = None
    nome_completo: str = Field(alias="nomeCompleto")
    data_nascimento: datetime = Field(alias="dataNascimento")
    cpf: str
    email: str
    nivel: str
    endereco: Endereco
    telefone: str
    idioma: Optional[str]
    tema: Optional[str]
    notificacoes: Optional[bool]
    foto_url: Optional[str]


    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class UsuarioCadastro(BaseModel):
    nome_completo: str = Field(alias="nomeCompleto")
    data_nascimento: datetime = Field(alias="dataNascimento")
    cpf: str
    email: str
    senha: str
    telefone: str
    endereco: Endereco

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True

class UsuarioEditar(BaseModel):
    nome_completo: Optional[str] = Field(alias="nomeCompleto")
    data_nascimento: Optional[datetime] = Field(alias="dataNascimento")
    senha: Optional[str]
    telefone: Optional[str]
    endereco: Optional[EnderecoEditar]
    idioma: Optional[str]
    tema: Optional[str]
    notificacoes: Optional[bool]
    foto_url: Optional[str]

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True
        orm_mode = True
