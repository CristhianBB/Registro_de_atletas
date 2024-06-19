import sys
import os

# Adiciona a raiz do projeto ao caminho do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel
from typing import Optional
from app import models, database

app = FastAPI()

# Certifique-se de que a importação acontece aqui, após resolver o caminho
from app.models import Atleta
from app.database import Base

# Cria as tabelas do banco de dados
Base.metadata.create_all(bind=database.engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
class AtletaCreate(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

class AtletaResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

@app.get("/atletas/", response_model=Page[AtletaResponse])
def get_atletas(
    nome: Optional[str] = Query(None), 
    cpf: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome == nome)
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return paginate(query.all())

@app.post("/atletas/", status_code=201, response_model=AtletaResponse)
def create_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    new_atleta = models.Atleta(**atleta.dict())
    try:
        db.add(new_atleta)
        db.commit()
        db.refresh(new_atleta)
        return AtletaResponse(
            id=new_atleta.id,
            nome=new_atleta.nome,
            cpf=new_atleta.cpf,
            centro_treinamento=new_atleta.centro_treinamento,
            categoria=new_atleta.categoria
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {new_atleta.cpf}"
        )

add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
