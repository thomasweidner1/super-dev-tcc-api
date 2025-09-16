from pydantic import BaseModel


class Endereco(BaseModel):
    rua: str
    numero: str
    cidade: str
    estado: str
    cep: str
