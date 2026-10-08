from fastapi import APIRouter, Depends
from dependecies import pegar_sessao
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from models import Pedido



#configs rota
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas rotas de pedidos precisam de autenticação.
    """
    return {"mensagem": "vc acessu pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario = pedido_schema.id_usuario) #olhar models do pedido, demais campos tem default
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"pedido criado com sucesso: {novo_pedido.usuario}"}