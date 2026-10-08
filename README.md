pip install fastapi uvicorn "sqlalchemy>=2.0,<2.1" passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart

app = FastAPI()
uvicorn main:app --reload

rotas: auth e order

APIRouter(prefix="/auth", tags=["auth"])
app.include_router(auth_router)


@order_router.get("/lista")
def funcao():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas rotas de pedidos precisam de autenticação.
    """

models.py
sqlalchemy: orm, traduzir python em sql
criação da tabela Usuario
pip install sqlalchemy_utils  
criação demais tabelas
pip install alembic
alembic init alembic
alembic.ini: target_metadata = Base.metadata
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

usuario.py
@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str):
def pegar_sessao():
pip install bcrypt==4.0.1
.env: SECRET_KEY = ""
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


schemas.py
class UsuarioSchema(BaseModel):
schemas aparece no fastapi/docs


@order_router.post("/pedido")

@auth_router.post("/login")