from fastapi import FastAPI
from passlib.context import CryptContext    # utilizada para hash e validação de senhas com bcrypt
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer   #para configurar autenticação OAuth2 via Bearer Token




load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))




app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    #usado para gerar e validar hashes de senha
oauth2_schema = OAuth2PasswordBearer(tokenUrl ="auth/login-form")   # Informa qual endpoint será responsável por realizar o login

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

