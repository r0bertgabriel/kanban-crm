from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VendedorLogin(BaseModel):
    nome: str
    senha: str

class VendedorResponse(BaseModel):
    id: int
    nome: str
    online: bool
    is_admin: bool = False
    
    class Config:
        from_attributes = True

class ClienteResponse(BaseModel):
    id: int
    nome: str
    celular: str
    email: str
    data_ultima_compra: datetime
    valor_total_compras: int
    status: str
    contatado: bool = False
    observacoes: Optional[str] = None
    dias_sem_comprar: Optional[int] = None
    vendedor_atribuido: Optional[str] = None
    
    class Config:
        from_attributes = True

class ContatoUpdate(BaseModel):
    cliente_id: int
    observacoes: Optional[str] = None

class RealocacaoCliente(BaseModel):
    cliente_id: int
    vendedor_id: int
