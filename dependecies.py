from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema






def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session   #alterenativa para o return, mas retorna valor sem encerrar a execução da def
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema),  session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))    #conf. def criar token => dic_info
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso negado, verifique validade do token")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="acesso invalido")
    return usuario