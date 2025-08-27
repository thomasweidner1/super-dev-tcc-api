# Função de dependência para obter uma sessçao do banco de dados
from src.super_api.database.banco_dados import SessionLocal


def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão de forma que o FastAPI possa utilizá-la nas rotas
    finally:
        db.close()  # Garante qeue a sessão será fechada após o uso

