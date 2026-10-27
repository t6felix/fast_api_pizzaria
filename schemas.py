#velocidade e integridade do sistema: padronização de recebimento de infos em um único objeto ao inves de varios parametros separados

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    class Config:   # para ser interpretado como orm, trasnformado em sql
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario: int

    class Config: 
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config: 
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config: 
        from_attributes = True