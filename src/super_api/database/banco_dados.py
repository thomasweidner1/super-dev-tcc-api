import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

# Carregar o arquivo .env com as configurações do banco de dados
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME", "super-tcc-db")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def popular_banco_dados():
    caminho_atual = Path(os.path.dirname(__file__))
    caminho_raiz = caminho_atual.parent.parent.parent
    # Lê e executa o arquivo SQL de seed
    sql_file = caminho_raiz / "db_seed.sql"
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";")

    with engine.connect() as conn:
        for sql_command in sql_commands:
            sql_command = sql_command.replace("\n", "")
            if not sql_command:
                continue
            conn.execute(text(sql_command + ";"))
            conn.commit()
        print("Dados inseridos com sucesso a partir de db_seed.sql")