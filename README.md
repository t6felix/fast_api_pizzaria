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

