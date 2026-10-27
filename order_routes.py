from fastapi import APIRouter, Depends, HTTPException
from dependecies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from models import Pedido, Usuario



#configs rota
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

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



@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="vc nao tem autorização para fazer esta modifcação")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"pedido numero {pedido.id} cancelado com sucesso",
            "pedido": pedido}