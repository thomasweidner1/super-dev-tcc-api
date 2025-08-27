from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.super_api.database.banco_dados import Base

class UsuarioEntidade(Base):

    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(50), nullable=False)
    data_nascimento: date = Column(Date(), nullable=False, name="data_nascimento")
    cpf = Column(String(14), nullable=False)
    email = Column(String(50), nullable=False)
    senha = Column(String, nullable=False)
    telefone = Column(String)
    #endereco = Column(Endereco, nullable=False)
    #cartao = Column(Cartao, nullable=False)
    #preferencias = Column(Preferencias)
    #foto_url = Column(String)
    nivel = Column(String, nullable=False)

    # id: number = 0,
    # nomeCompleto: string = '',
    # dataNascimento: Date = new
    # Date(),
    # cpf: string = '',
    # email: string = '',
    # senha: string = '',
    # telefone: string = '',
    # endereco: Endereco = new
    # Endereco(),
    # cartao: Cartao = new
    # Cartao(),
    # preferencias?: Preferencias,
    # fotoUrl: string = '',
    # nivel: string = '',

    # matriculas = relationship("MatriculaEntidade", back_populates="curso")



# class CursoEntidade(Base):
#     # Criar tabela
#     __tablename__ = "cursos"
#
#     id = Column(Integer, primary_key=True, index=True)
#     nome = Column(String(50), nullable=False)
#     sigla = Column(String(3), nullable=False)
#
#     matriculas = relationship("MatriculaEntidade", back_populates="curso")
#
# class AlunoEntidade(Base):
#     __tablename__ = "alunos"
#
#     id: int = Column(Integer, primary_key=True, index=True)
#     nome: str = Column(String(20), nullable=False)
#     sobrenome: str = Column(String(50), nullable=False)
#     cpf: str = Column(String(14), nullable=False)
#     data_nascimento: date = Column(Date(), nullable=False, name="data_nascimento")
#
#     matriculas = relationship("MatriculaEntidade", back_populates="aluno")
#
# class MatriculaEntidade(Base):
#     __tablename__ = "matriculas"
#
#     id: int = Column(Integer, primary_key=True, index=True)
#     aluno_id: int = Column(Integer, ForeignKey("alunos.id"), nullable=False)
#     curso_id: int = Column(Integer, ForeignKey(CursoEntidade.id), nullable=False)
#     data_matricula: date = Column(Date, nullable=True, default=date.today)
#
#     # relacionamentos permite acessa m.aluno e m.curso
#     aluno = relationship("AlunoEntidade", back_populates="matriculas", lazy='joined')
#     curso = relationship("CursoEntidade", back_populates="matriculas", lazy='joined')
#
