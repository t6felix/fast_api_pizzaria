from sqlalchemy.orm import sessionmaker
from models import db

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session   #alterenativa para o return, mas retorna valor sem encerrar a execução da def
    finally:
        session.close()