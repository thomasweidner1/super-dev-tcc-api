from datetime import datetime
from pydantic import BaseModel, Field
from src.super_api.schemas.endereco_schema import Endereco


class Usuario(BaseModel):
    id: int | None = None
    nome_completo: str = Field(alias="nomeCompleto")
    data_nascimento: datetime = Field(alias="dataNascimento")
    cpf: str
    email: str
    senha: str
    nivel: str
    endereco: Endereco

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class UsuarioCadastro(BaseModel):
    nome_completo: str = Field(alias="nomeCompleto")
    data_nascimento: datetime = Field(alias="dataNascimento")
    cpf: str
    email: str
    senha: str
    endereco: Endereco

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


# class AlunoCadastro(BaseModel):
#     nome: str = Field()
#     sobrenome: str = Field()
#     cpf: str = Field()
#     data_nascimento: datetime = Field(alias="dataNascimento")
#     class Config:
#         allow_population_by_field_name = True
#
#
# class AlunoEditar(BaseModel):
#     nome: str = Field()
#     sobrenome: str = Field()
#     cpf: str = Field()
#     data_nascimento: datetime = Field(alias="dataNascimento")
#     class Config:
#         allow_population_by_field_name = True