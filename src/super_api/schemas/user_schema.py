from datetime import datetime

from pydantic import BaseModel, Field


# class Aluno(BaseModel):
#     id: int = Field()
#     nome: str = Field()
#     sobrenome: str = Field()
#     cpf: str = Field()
#     data_nascimento: datetime = Field(alias="dataNascimento")
#
#     class Config:
#         populate_by_name = True
#         allow_population_by_field_name = True
#
#
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