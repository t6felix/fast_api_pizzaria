from fastapi import APIRouter, Depends, HTTPException
from dependecies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session
from models import Pedido, Usuario, ItemPedido



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



@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="vc nao tem autorização para realizar esta ação")
    else:
        pedidos = session.query(Pedido).all()
        return {"pedidos": pedidos}



@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="vc nao tem autorização para fazer esta operação")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{"mensagem": "item criado com sucesso",
            "item_id": item_pedido.id,
            "preco_pedido": pedido.preco}



@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="item do pedido nao existent")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="vc nao tem autorização para fazer esta operação")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{"mensagem": "item removido com sucesso",
            "itens_pedido":pedido.itens,
            # "qtd_itens_pedido": len(pedido.itens),
            "pedido": pedido}



@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="vc nao tem autorização para fazer esta modifcação")
    pedido.status = "FINALIZADO"
    session.commit()
    return {"mensagem": f"pedido numero {pedido.id} finalziado com sucesso",
            "pedido": pedido}



@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int,session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail="vc nao tem autorização para fazer esta modifcação")
    return {
        "qtd_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }



@order_router.get("/listar/{pedidos-usuario}")      # do usuario logado
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return {"pedidos": pedidos}