from pydantic import BaseModel, Field


class Endereco(BaseModel):
    rua: str
    numero: str
    cidade: str
    estado: str
    cep: str = Field(default="")
