from datetime import datetime, timedelta
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.models import Cliente, ClienteVendedor, Vendedor
from backend.models.schemas import ClienteResponse, RealocacaoCliente
from backend.utils.distribuicao import get_clientes_por_periodo, redistribuir_clientes

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/clientes-por-periodo")
async def clientes_por_periodo(db: Session = Depends(get_db)):
    """Retorna todos os clientes organizados por período de inatividade"""
    return get_clientes_por_periodo(db)

@router.get("/todos-clientes")
async def get_todos_clientes(db: Session = Depends(get_db)):
    """Retorna todos os clientes com informações de atribuição"""
    clientes = db.query(Cliente).all()
    hoje = datetime.now()
    resultado = []
    
    for cliente in clientes:
        dias_sem_comprar = (hoje - cliente.data_ultima_compra).days
        
        # Buscar atribuição atual
        atribuicao = db.query(ClienteVendedor).filter(
            ClienteVendedor.cliente_id == cliente.id,
            ClienteVendedor.contatado == False
        ).first()
        
        vendedor_nome = None
        contatado = False
        observacoes = None
        
        if atribuicao:
            vendedor = db.query(Vendedor).filter(Vendedor.id == atribuicao.vendedor_id).first()
            if vendedor:
                vendedor_nome = vendedor.nome
            contatado = atribuicao.contatado
            observacoes = atribuicao.observacoes
        
        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "celular": cliente.celular,
            "email": cliente.email,
            "data_ultima_compra": cliente.data_ultima_compra,
            "valor_total_compras": cliente.valor_total_compras,
            "status": cliente.status,
            "dias_sem_comprar": dias_sem_comprar,
            "vendedor_atribuido": vendedor_nome,
            "contatado": contatado,
            "observacoes": observacoes
        })
    
    return resultado

@router.post("/realocar-cliente")
async def realocar_cliente(realocacao: RealocacaoCliente, db: Session = Depends(get_db)):
    """Realoca um cliente para outro vendedor"""
    # Verificar se o cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == realocacao.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se o vendedor existe e não é admin
    vendedor = db.query(Vendedor).filter(
        Vendedor.id == realocacao.vendedor_id,
        Vendedor.is_admin == False
    ).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    # Remover atribuição anterior não contatada
    db.query(ClienteVendedor).filter(
        ClienteVendedor.cliente_id == realocacao.cliente_id,
        ClienteVendedor.contatado == False
    ).delete()
    
    # Criar nova atribuição
    nova_atribuicao = ClienteVendedor(
        cliente_id=realocacao.cliente_id,
        vendedor_id=realocacao.vendedor_id,
        data_atribuicao=datetime.now()
    )
    db.add(nova_atribuicao)
    
    cliente.status = "atribuido"
    db.commit()
    
    return {"message": f"Cliente realocado para {vendedor.nome}"}

@router.post("/redistribuir-todos")
async def redistribuir_todos_clientes(db: Session = Depends(get_db)):
    """Force redistribuição de todos os clientes disponíveis"""
    # Limpar todas as atribuições não contatadas
    db.query(ClienteVendedor).filter(ClienteVendedor.contatado == False).delete()
    
    # Marcar todos os clientes elegíveis como disponíveis
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=60)
    data_fim = hoje - timedelta(days=30)
    
    clientes_elegiveis = db.query(Cliente).filter(
        Cliente.data_ultima_compra >= data_inicio,
        Cliente.data_ultima_compra <= data_fim,
        Cliente.status != "contatado"
    ).all()
    
    for cliente in clientes_elegiveis:
        cliente.status = "disponivel"
    
    db.commit()
    
    # Redistribuir
    redistribuir_clientes(db)
    
    return {"message": "Redistribuição realizada com sucesso"}

@router.get("/estatisticas-gerais")
async def get_estatisticas_gerais(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais do sistema"""
    hoje = datetime.now()
    
    # Total de clientes
    total_clientes = db.query(Cliente).count()
    
    # Clientes por status
    clientes_disponiveis = db.query(Cliente).filter(Cliente.status == "disponivel").count()
    clientes_atribuidos = db.query(Cliente).filter(Cliente.status == "atribuido").count()
    clientes_contatados = db.query(Cliente).filter(Cliente.status == "contatado").count()
    
    # Clientes por período
    data_30 = hoje - timedelta(days=30)
    data_60 = hoje - timedelta(days=60)
    data_90 = hoje - timedelta(days=90)
    
    clientes_30_60 = db.query(Cliente).filter(
        Cliente.data_ultima_compra >= data_60,
        Cliente.data_ultima_compra <= data_30
    ).count()
    
    clientes_60_90 = db.query(Cliente).filter(
        Cliente.data_ultima_compra >= data_90,
        Cliente.data_ultima_compra < data_60
    ).count()
    
    clientes_mais_90 = db.query(Cliente).filter(
        Cliente.data_ultima_compra < data_90
    ).count()
    
    # Vendedores online
    vendedores_online = db.query(Vendedor).filter(
        Vendedor.online == True,
        Vendedor.is_admin == False
    ).count()
    
    # Performance dos vendedores
    vendedores = db.query(Vendedor).filter(Vendedor.is_admin == False).all()
    performance_vendedores = []
    
    for vendedor in vendedores:
        total_atribuidos = db.query(ClienteVendedor).filter(
            ClienteVendedor.vendedor_id == vendedor.id
        ).count()
        
        total_contatados = db.query(ClienteVendedor).filter(
            ClienteVendedor.vendedor_id == vendedor.id,
            ClienteVendedor.contatado == True
        ).count()
        
        taxa_conversao = (total_contatados / total_atribuidos * 100) if total_atribuidos > 0 else 0
        
        performance_vendedores.append({
            "nome": vendedor.nome,
            "online": vendedor.online,
            "total_atribuidos": total_atribuidos,
            "total_contatados": total_contatados,
            "taxa_conversao": round(taxa_conversao, 2)
        })
    
    return {
        "total_clientes": total_clientes,
        "clientes_disponiveis": clientes_disponiveis,
        "clientes_atribuidos": clientes_atribuidos,
        "clientes_contatados": clientes_contatados,
        "clientes_30_60_dias": clientes_30_60,
        "clientes_60_90_dias": clientes_60_90,
        "clientes_mais_90_dias": clientes_mais_90,
        "vendedores_online": vendedores_online,
        "performance_vendedores": performance_vendedores
    }

@router.post("/liberar-cliente/{cliente_id}")
async def liberar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Libera um cliente de sua atribuição atual"""
    # Remover atribuição não contatada
    db.query(ClienteVendedor).filter(
        ClienteVendedor.cliente_id == cliente_id,
        ClienteVendedor.contatado == False
    ).delete()
    
    # Atualizar status do cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente and cliente.status != "contatado":
        cliente.status = "disponivel"
    
    db.commit()
    
    return {"message": "Cliente liberado com sucesso"}
