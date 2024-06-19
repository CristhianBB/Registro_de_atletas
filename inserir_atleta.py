from app.models import Atleta
from app.database import SessionLocal

def obter_dados_atleta():
    nome = input("Digite o nome do atleta: ")
    cpf = input("Digite o CPF do atleta: ")
    centro_treinamento = input("Digite o centro de treinamento do atleta: ")
    categoria = input("Digite a categoria do atleta: ")

    return {
        "nome": nome,
        "cpf": cpf,
        "centro_treinamento": centro_treinamento,
        "categoria": categoria
    }

def inserir_atleta():
    db = SessionLocal()
    try:
        dados_atleta = obter_dados_atleta()
        db_atleta = Atleta(**dados_atleta)
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
        print("Atleta inserido com sucesso:")
        print(f"ID: {db_atleta.id}, Nome: {db_atleta.nome}, CPF: {db_atleta.cpf}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao inserir atleta: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inserir_atleta()
