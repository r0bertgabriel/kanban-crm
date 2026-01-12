from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.models import Cliente, ClienteVendedor, Vendedor
from backend.models.schemas import ClienteResponse, ContatoUpdate
from backend.utils.distribuicao import redistribuir_clientes

router = APIRouter(prefix="/api/vendedor", tags=["Vendedor"])

@router.get("/meus-clientes/{vendedor_id}", response_model=List[ClienteResponse])
async def get_meus_clientes(vendedor_id: int, db: Session = Depends(get_db)):
    """Retorna clientes atribuídos ao vendedor"""
    atribuicoes = db.query(ClienteVendedor).filter(
        ClienteVendedor.vendedor_id == vendedor_id,
        ClienteVendedor.contatado == False
    ).all()
    
    clientes = []
    hoje = datetime.now()
    
    for atrib in atribuicoes:
        cliente = db.query(Cliente).filter(Cliente.id == atrib.cliente_id).first()
        if cliente:
            dias_sem_comprar = (hoje - cliente.data_ultima_compra).days
            cliente_dict = {
                "id": cliente.id,
                "nome": cliente.nome,
                "celular": cliente.celular,
                "email": cliente.email,
                "data_ultima_compra": cliente.data_ultima_compra,
                "valor_total_compras": cliente.valor_total_compras,
                "status": cliente.status,
                "contatado": atrib.contatado,
                "observacoes": atrib.observacoes,
                "dias_sem_comprar": dias_sem_comprar
            }
            clientes.append(cliente_dict)
    
    return clientes

@router.post("/marcar-contatado/{vendedor_id}")
async def marcar_contatado(vendedor_id: int, contato: ContatoUpdate, db: Session = Depends(get_db)):
    """Marca cliente como contatado"""
    atribuicao = db.query(ClienteVendedor).filter(
        ClienteVendedor.cliente_id == contato.cliente_id,
        ClienteVendedor.vendedor_id == vendedor_id,
        ClienteVendedor.contatado == False
    ).first()
    
    if not atribuicao:
        raise HTTPException(status_code=404, detail="Cliente não encontrado ou já contatado")
    
    atribuicao.contatado = True
    atribuicao.data_contato = datetime.now()
    atribuicao.observacoes = contato.observacoes
    
    cliente = db.query(Cliente).filter(Cliente.id == contato.cliente_id).first()
    if cliente:
        cliente.status = "contatado"
    
    db.commit()
    
    return {"message": "Cliente marcado como contatado"}

@router.get("/estatisticas/{vendedor_id}")
async def get_estatisticas(vendedor_id: int, db: Session = Depends(get_db)):
    """Retorna estatísticas do vendedor"""
    total_atribuidos = db.query(ClienteVendedor).filter(
        ClienteVendedor.vendedor_id == vendedor_id
    ).count()
    
    total_contatados = db.query(ClienteVendedor).filter(
        ClienteVendedor.vendedor_id == vendedor_id,
        ClienteVendedor.contatado == True
    ).count()
    
    total_pendentes = db.query(ClienteVendedor).filter(
        ClienteVendedor.vendedor_id == vendedor_id,
        ClienteVendedor.contatado == False
    ).count()
    
    return {
        "total_atribuidos": total_atribuidos,
        "total_contatados": total_contatados,
        "total_pendentes": total_pendentes
    }
