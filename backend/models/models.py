from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Vendedor(Base):
    __tablename__ = "vendedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    senha = Column(String)
    online = Column(Boolean, default=False)
    ultimo_acesso = Column(DateTime, default=datetime.now)
    is_admin = Column(Boolean, default=False)
    clientes = relationship("ClienteVendedor", back_populates="vendedor")

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    celular = Column(String, unique=True)
    email = Column(String)
    data_ultima_compra = Column(DateTime)
    valor_total_compras = Column(Integer, default=0)
    status = Column(String, default="disponivel")  # disponivel, atribuido, contatado
    vendedores = relationship("ClienteVendedor", back_populates="cliente")

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Integer)
    categoria = Column(String)

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    data_pedido = Column(DateTime)
    valor = Column(Integer)
    quantidade = Column(Integer)

class ClienteVendedor(Base):
    __tablename__ = "cliente_vendedor"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"))
    data_atribuicao = Column(DateTime, default=datetime.now)
    contatado = Column(Boolean, default=False)
    data_contato = Column(DateTime, nullable=True)
    observacoes = Column(String, nullable=True)
    
    cliente = relationship("Cliente", back_populates="vendedores")
    vendedor = relationship("Vendedor", back_populates="clientes")
