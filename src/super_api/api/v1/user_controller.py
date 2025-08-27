from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.super_api.app import router
from src.super_api.dependencias import get_db

# @router.get("/api/usuarios", tags=['usuarios'])
# def obter_todos_alunos(db: Session = Depends(get_db)):
#     usuarios = db.query()

# @router.get("/api/alunos", tags=["alunos"])
# def obter_todos_alunos(db: Session = Depends(get_db)):
#     alunos = db.query(AlunoEntidade).all()
#     alunos_response = [Aluno(
#         id=aluno.id,
#         nome=aluno.nome,
#         sobrenome=aluno.sobrenome,
#         cpf=aluno.cpf,
#         data_nascimento=aluno.data_nascimento,
#     ) for aluno in alunos]
#     return alunos_response