from fastapi import APIRouter

#configs rota
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "vc acessu auth"}