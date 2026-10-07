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