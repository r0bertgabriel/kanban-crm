import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from backend.models.models import Cliente, ClienteVendedor, Pedido, Produto, Vendedor


def populate_database(db: Session):
    """Popula o banco de dados com dados fictícios"""
    fake = Faker('pt_BR')
    
    # Limpar dados existentes
    db.query(ClienteVendedor).delete()
    db.query(Pedido).delete()
    db.query(Cliente).delete()
    db.query(Produto).delete()
    db.query(Vendedor).delete()
    
    # Criar administrador
    admin = Vendedor(
        nome="Admin",
        senha="admin123",
        online=False,
        is_admin=True
    )
    db.add(admin)
    
    # Criar vendedores
    vendedores_nomes = ["João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Ferreira"]
    vendedores = []
    for nome in vendedores_nomes:
        vendedor = Vendedor(nome=nome, senha="123456", online=False, is_admin=False)
        db.add(vendedor)
        vendedores.append(vendedor)
    db.commit()
    
    # Criar produtos
    produtos_lista = [
        {"nome": "Notebook Dell", "preco": 350000, "categoria": "Eletrônicos"},
        {"nome": "Mouse Logitech", "preco": 15000, "categoria": "Periféricos"},
        {"nome": "Teclado Mecânico", "preco": 45000, "categoria": "Periféricos"},
        {"nome": "Monitor LG 27\"", "preco": 120000, "categoria": "Eletrônicos"},
        {"nome": "Webcam Full HD", "preco": 25000, "categoria": "Periféricos"},
        {"nome": "Headset Gamer", "preco": 35000, "categoria": "Áudio"},
        {"nome": "SSD 1TB", "preco": 55000, "categoria": "Armazenamento"},
        {"nome": "Memória RAM 16GB", "preco": 30000, "categoria": "Hardware"},
        {"nome": "Placa de Vídeo RTX", "preco": 450000, "categoria": "Hardware"},
        {"nome": "Cadeira Gamer", "preco": 120000, "categoria": "Móveis"},
    ]
    
    produtos = []
    for prod in produtos_lista:
        produto = Produto(**prod)
        db.add(produto)
        produtos.append(produto)
    db.commit()
    
    # Criar clientes
    hoje = datetime.now()
    clientes = []
    celulares_usados = set()
    
    # Clientes que não compraram entre 30 e 45 dias (PRIORIDADE ALTA - 30 clientes)
    for i in range(30):
        dias_atras = random.randint(30, 45)
        data_ultima_compra = hoje - timedelta(days=dias_atras)
        
        # Gerar número de celular único
        while True:
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '91'])
            celular = f"+55{ddd}9{random.randint(10000000, 99999999)}"
            if celular not in celulares_usados:
                celulares_usados.add(celular)
                break
        
        cliente = Cliente(
            nome=fake.name(),
            celular=celular,
            email=fake.email(),
            data_ultima_compra=data_ultima_compra,
            valor_total_compras=random.randint(50000, 500000),
            status="disponivel"
        )
        db.add(cliente)
        clientes.append(cliente)
        
        # Criar pedidos históricos para este cliente
        num_pedidos = random.randint(2, 8)
        for j in range(num_pedidos):
            dias_pedido = random.randint(dias_atras, dias_atras + 180)
            pedido = Pedido(
                cliente_id=cliente.id,
                produto_id=random.choice(produtos).id,
                data_pedido=hoje - timedelta(days=dias_pedido),
                valor=random.randint(10000, 100000),
                quantidade=random.randint(1, 5)
            )
            db.add(pedido)
    
    # Clientes que não compraram entre 45 e 60 dias (PRIORIDADE MÉDIA - 25 clientes)
    for i in range(25):
        dias_atras = random.randint(45, 60)
        data_ultima_compra = hoje - timedelta(days=dias_atras)
        
        while True:
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '91'])
            celular = f"+55{ddd}9{random.randint(10000000, 99999999)}"
            if celular not in celulares_usados:
                celulares_usados.add(celular)
                break
        
        cliente = Cliente(
            nome=fake.name(),
            celular=celular,
            email=fake.email(),
            data_ultima_compra=data_ultima_compra,
            valor_total_compras=random.randint(50000, 500000),
            status="disponivel"
        )
        db.add(cliente)
        clientes.append(cliente)
        
        # Criar pedidos históricos
        num_pedidos = random.randint(2, 6)
        for j in range(num_pedidos):
            dias_pedido = random.randint(dias_atras, dias_atras + 180)
            pedido = Pedido(
                cliente_id=cliente.id,
                produto_id=random.choice(produtos).id,
                data_pedido=hoje - timedelta(days=dias_pedido),
                valor=random.randint(10000, 100000),
                quantidade=random.randint(1, 5)
            )
            db.add(pedido)
    
    # Alguns clientes que compraram recentemente (não devem aparecer na lista prioritária)
    for i in range(20):
        dias_atras = random.randint(1, 29)
        data_ultima_compra = hoje - timedelta(days=dias_atras)
        
        while True:
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '91'])
            celular = f"+55{ddd}9{random.randint(10000000, 99999999)}"
            if celular not in celulares_usados:
                celulares_usados.add(celular)
                break
        
        cliente = Cliente(
            nome=fake.name(),
            celular=celular,
            email=fake.email(),
            data_ultima_compra=data_ultima_compra,
            valor_total_compras=random.randint(50000, 500000),
            status="ativo"
        )
        db.add(cliente)
    
    # Clientes que não compraram há muito tempo (60-90 dias - 20 clientes)
    for i in range(20):
        dias_atras = random.randint(60, 90)
        data_ultima_compra = hoje - timedelta(days=dias_atras)
        
        while True:
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '91'])
            celular = f"+55{ddd}9{random.randint(10000000, 99999999)}"
            if celular not in celulares_usados:
                celulares_usados.add(celular)
                break
        
        cliente = Cliente(
            nome=fake.name(),
            celular=celular,
            email=fake.email(),
            data_ultima_compra=data_ultima_compra,
            valor_total_compras=random.randint(50000, 500000),
            status="disponivel"
        )
        db.add(cliente)
    
    # Clientes muito inativos (mais de 90 dias - 15 clientes)
    for i in range(15):
        dias_atras = random.randint(91, 365)
        data_ultima_compra = hoje - timedelta(days=dias_atras)
        
        while True:
            ddd = random.choice(['11', '21', '31', '41', '51', '61', '71', '81', '85', '91'])
            celular = f"+55{ddd}9{random.randint(10000000, 99999999)}"
            if celular not in celulares_usados:
                celulares_usados.add(celular)
                break
        
        cliente = Cliente(
            nome=fake.name(),
            celular=celular,
            email=fake.email(),
            data_ultima_compra=data_ultima_compra,
            valor_total_compras=random.randint(50000, 500000),
            status="inativo"
        )
        db.add(cliente)
    
    db.commit()
    print("✅ Banco de dados populado com sucesso!")
    print(f"   📊 Total de clientes: {db.query(Cliente).count()}")
    print(f"   👥 Vendedores: {len(vendedores_nomes)}")
    print(f"   🎯 Clientes prioritários (30-60 dias): 55")
