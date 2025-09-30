from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.super_api.database.banco_dados import Base

class UsuarioEntidade(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(50), nullable=False)
    data_nascimento: Date = Column(Date(), nullable=False, name="data_nascimento")
    cpf = Column(String(14), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    senha = Column(String(500), nullable=False)
    telefone = Column(String(50), nullable=True)
    nivel = Column(String(50), nullable=True, default="comum", server_default="comum")
    foto_url = Column(String(500))
    #preferencias
    idioma = Column(String(50), default="pt_br", server_default="pt_br")
    tema = Column(String(50), default="claro", server_default="claro")
    notificacoes = Column(Boolean, default=False)

    # Um usuário pode ter vários endereços
    enderecos = relationship("EnderecoEntidade", back_populates="usuario")
    # Um usuário pode ter várias hospedagens cadastradas
    hospedagens = relationship("HospedagemEntidade", back_populates="usuario")
    # Um usuário pode ter vários cartoes
    cartoes = relationship("CartaoEntidade", back_populates="usuario")

class EnderecoEntidade(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True)
    rua = Column(String(100), nullable=False)
    numero = Column(String(20), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False)
    complemento = Column(String(500))
    bairro = Column(String(50))
    cep = Column(String(9))

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("UsuarioEntidade", back_populates="enderecos")

    # Um endereço pode ter zero ou uma hospedagem
    hospedagem = relationship("HospedagemEntidade", back_populates="endereco", uselist=False)

class CartaoEntidade(Base):
    __tablename__ = "cartoes"

    id = Column(Integer, primary_key=True)
    numero = Column(String(16), nullable=False)
    nome_titular = Column(String(50), nullable=False)
    validade: Date = Column(Date(), nullable=False, name="validade")
    cvv = Column(String(3), nullable=False)
    cpf_tituar = Column(String(14), nullable=False, unique=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("UsuarioEntidade", back_populates="cartoes")

class HospedagemEntidade(Base):
    __tablename__ = "hospedagens"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=False)

    usuario = relationship("UsuarioEntidade", back_populates="hospedagens")
    endereco = relationship("EnderecoEntidade", back_populates="hospedagem")

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
