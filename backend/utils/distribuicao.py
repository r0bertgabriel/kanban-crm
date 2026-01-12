import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.models.models import Cliente, ClienteVendedor, Vendedor


def redistribuir_clientes(db: Session):
    """
    Redistribui clientes disponíveis entre vendedores online.
    Corrige o bug: busca todos os clientes elegíveis, não apenas os com status 'pendente'
    """
    # Buscar vendedores online (não admin)
    vendedores_online = db.query(Vendedor).filter(
        Vendedor.online == True,
        Vendedor.is_admin == False
    ).all()
    
    if not vendedores_online:
        return
    
    # Buscar clientes que devem ser contatados (30-60 dias sem comprar)
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=60)
    data_fim = hoje - timedelta(days=30)
    
    # Limpar atribuições antigas de vendedores offline que não foram contatados
    vendedores_offline_ids = db.query(Vendedor.id).filter(
        Vendedor.online == False,
        Vendedor.is_admin == False
    ).all()
    vendedores_offline_ids = [v[0] for v in vendedores_offline_ids]
    
    if vendedores_offline_ids:
        # Deletar atribuições de vendedores offline
        db.query(ClienteVendedor).filter(
            ClienteVendedor.vendedor_id.in_(vendedores_offline_ids),
            ClienteVendedor.contatado == False
        ).delete(synchronize_session=False)
        db.commit()
    
    # Buscar clientes elegíveis (30-60 dias) que ainda não foram contatados
    clientes_elegiveis = db.query(Cliente).filter(
        Cliente.data_ultima_compra >= data_inicio,
        Cliente.data_ultima_compra <= data_fim,
        Cliente.status != "contatado"
    ).all()
    
    # Separar clientes que já estão atribuídos dos disponíveis
    clientes_com_atribuicao = []
    clientes_disponiveis = []
    
    for cliente in clientes_elegiveis:
        atribuicao_ativa = db.query(ClienteVendedor).filter(
            ClienteVendedor.cliente_id == cliente.id,
            ClienteVendedor.contatado == False
        ).first()
        
        if atribuicao_ativa:
            # Verificar se o vendedor está online
            vendedor = db.query(Vendedor).filter(Vendedor.id == atribuicao_ativa.vendedor_id).first()
            if vendedor and vendedor.online:
                clientes_com_atribuicao.append(cliente)
            else:
                clientes_disponiveis.append(cliente)
                cliente.status = "disponivel"
        else:
            clientes_disponiveis.append(cliente)
            cliente.status = "disponivel"
    
    # Distribuir clientes disponíveis entre vendedores online
    if clientes_disponiveis:
        num_vendedores = len(vendedores_online)
        # Embaralhar para distribuição justa
        random.shuffle(clientes_disponiveis)
        
        for idx, cliente in enumerate(clientes_disponiveis):
            vendedor = vendedores_online[idx % num_vendedores]
            
            # Criar nova atribuição
            atribuicao = ClienteVendedor(
                cliente_id=cliente.id,
                vendedor_id=vendedor.id,
                data_atribuicao=datetime.now()
            )
            db.add(atribuicao)
            cliente.status = "atribuido"
    
    db.commit()

def get_clientes_por_periodo(db: Session):
    """
    Retorna clientes organizados por período de inatividade
    """
    hoje = datetime.now()
    
    periodos = {
        "30_45_dias": {"inicio": hoje - timedelta(days=45), "fim": hoje - timedelta(days=30)},
        "45_60_dias": {"inicio": hoje - timedelta(days=60), "fim": hoje - timedelta(days=45)},
        "60_90_dias": {"inicio": hoje - timedelta(days=90), "fim": hoje - timedelta(days=60)},
        "mais_90_dias": {"inicio": hoje - timedelta(days=365), "fim": hoje - timedelta(days=90)},
    }
    
    resultado = {}
    
    for periodo_nome, datas in periodos.items():
        clientes = db.query(Cliente).filter(
            Cliente.data_ultima_compra >= datas["inicio"],
            Cliente.data_ultima_compra <= datas["fim"]
        ).all()
        
        resultado[periodo_nome] = []
        for cliente in clientes:
            dias_sem_comprar = (hoje - cliente.data_ultima_compra).days
            
            # Buscar atribuição atual
            atribuicao = db.query(ClienteVendedor).filter(
                ClienteVendedor.cliente_id == cliente.id,
                ClienteVendedor.contatado == False
            ).first()
            
            vendedor_nome = None
            if atribuicao:
                vendedor = db.query(Vendedor).filter(Vendedor.id == atribuicao.vendedor_id).first()
                if vendedor:
                    vendedor_nome = vendedor.nome
            
            resultado[periodo_nome].append({
                "id": cliente.id,
                "nome": cliente.nome,
                "celular": cliente.celular,
                "email": cliente.email,
                "data_ultima_compra": cliente.data_ultima_compra,
                "valor_total_compras": cliente.valor_total_compras,
                "status": cliente.status,
                "dias_sem_comprar": dias_sem_comprar,
                "vendedor_atribuido": vendedor_nome,
                "contatado": atribuicao.contatado if atribuicao else False,
                "observacoes": atribuicao.observacoes if atribuicao else None
            })
    
    return resultado
