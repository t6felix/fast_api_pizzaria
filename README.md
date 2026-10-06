pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart

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