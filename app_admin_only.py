"""
Painel Vendedor - SISTEMA EXCLUSIVO ADMINISTRADOR
Sistema avançado com distribuição customizável por atributos
Vendedores são apenas identificadores numéricos, sem login
"""
import io
import json
import random
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List, Optional

from faker import Faker
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ==================== DATABASE ====================
DATABASE_URL = "sqlite:///./crm_admin_only.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== MODELS ====================
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email = Column(String, nullable=False)
    data_ultima_compra = Column(DateTime, nullable=False)
    valor_total_compras = Column(Float, default=0.0)
    status = Column(String, default="disponivel")  # disponivel, atribuido, contatado
    vendedor_id = Column(Integer, nullable=True)  # ID numérico do vendedor atual (1, 2, 3...)
    vendedor_anterior_id = Column(Integer, nullable=True)  # Último vendedor que atendeu
    data_atribuicao = Column(DateTime, nullable=True)
    contatado = Column(Boolean, default=False)
    data_contato = Column(DateTime, nullable=True)
    observacoes = Column(Text, nullable=True)
    # Atributos customizáveis para distribuição
    prioridade = Column(Integer, default=0)  # 0-10, quanto maior mais importante

class ConfiguracaoSistema(Base):
    __tablename__ = "configuracoes"
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String, unique=True, nullable=False)
    valor = Column(Text, nullable=False)
    descricao = Column(String, nullable=True)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

# ==================== SCHEMAS ====================
class LoginRequest(BaseModel):
    usuario: str
    senha: str

class ClienteResponse(BaseModel):
    id: int
    nome: str
    celular: str
    email: str
    data_ultima_compra: datetime
    valor_total_compras: float
    dias_sem_comprar: int
    periodo: str
    vendedor_id: Optional[int]
    vendedor_anterior_id: Optional[int]
    contatado: bool
    observacoes: Optional[str]
    prioridade: int

class DistribuicaoConfig(BaseModel):
    num_vendedores: int
    atributo_peso: str  # 'prioridade', 'dias_sem_comprar', 'valor_total', 'vendedor_anterior'
    pesos_vendedores: List[float]  # Lista de pesos para cada vendedor (ex: [1.0, 1.5, 0.8] = vendedor 2 pega 50% a mais)
    priorizar_vendedor_anterior: bool = True  # Se True, prioriza cliente para vendedor que já atendeu

class ClienteUpdate(BaseModel):
    prioridade: Optional[int] = None
    observacoes: Optional[str] = None

# ==================== DATABASE DEPENDENCY ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== POPULATE DATABASE ====================
def popular_banco(db: Session):
    """Popula banco com dados fictícios brasileiros"""
    # Verificar se já existe dados
    if db.query(Cliente).count() > 0:
        return
    
    fake = Faker('pt_BR')
    hoje = datetime.now()
    
    # Criar admin
    admin = Admin(usuario="admin", senha="admin123")
    db.add(admin)
    
    # Criar configuração padrão
    config = ConfiguracaoSistema(
        chave="num_vendedores",
        valor="5",
        descricao="Número de vendedores ativos no sistema"
    )
    db.add(config)
    
    # Criar clientes com atributos variados
    periodos = [
        (30, 45, 40),   # Urgente: 40 clientes
        (45, 60, 35),   # Atenção: 35 clientes
        (60, 90, 25),   # Moderado: 25 clientes
        (90, 180, 20),  # Crítico: 20 clientes
        (0, 30, 30),    # Ativos: 30 clientes
    ]
    
    ddds = ['11', '21', '31', '41', '51', '61', '71', '81', '85', '91']
    
    for dias_min, dias_max, quantidade in periodos:
        for _ in range(quantidade):
            dias_atras = random.randint(dias_min, dias_max)
            data_compra = hoje - timedelta(days=dias_atras)
            
            ddd = random.choice(ddds)
            numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular = f"({ddd}) {numero}"
            
            valor_total = round(random.uniform(500, 25000), 2)
            
            # Simular histórico: alguns clientes têm vendedor anterior
            vendedor_anterior = random.choice([None, None, None, 1, 2, 3, 4, 5]) if random.random() > 0.5 else None
            
            cliente = Cliente(
                nome=fake.name(),
                celular=celular,
                email=fake.email(),
                data_ultima_compra=data_compra,
                valor_total_compras=valor_total,
                status="disponivel",
                vendedor_anterior_id=vendedor_anterior,
                # Atributos customizáveis
                prioridade=random.randint(0, 10)
            )
            db.add(cliente)
    
    db.commit()
    print(f"✅ Banco populado: 150 clientes, 1 admin, sistema configurado")

# ==================== LIFESPAN ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        popular_banco(db)
    finally:
        db.close()
    yield
    # Shutdown (se necessário)

# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Painel Vendedor - Admin Only",
    description="Sistema avançado exclusivo para administrador com distribuição customizável",
    version="4.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROUTES ====================
@app.get("/")
async def root():
    return FileResponse("static/admin_advanced.html")

@app.post("/api/login")
async def login(login: LoginRequest, db: Session = Depends(get_db)):
    """Login do administrador"""
    admin = db.query(Admin).filter(
        Admin.usuario == login.usuario,
        Admin.senha == login.senha
    ).first()
    
    if not admin:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {"message": "Login realizado com sucesso", "usuario": admin.usuario}

@app.get("/api/clientes")
async def listar_clientes(db: Session = Depends(get_db)):
    """Lista todos os clientes com informações completas"""
    clientes = db.query(Cliente).all()
    hoje = datetime.now()
    resultado = []
    
    for cliente in clientes:
        dias = (hoje - cliente.data_ultima_compra).days
        
        # Determinar período
        if dias < 30:
            periodo = "Ativo"
        elif dias <= 45:
            periodo = "🔥 Urgente (30-45d)"
        elif dias <= 60:
            periodo = "⚠️ Atenção (45-60d)"
        elif dias <= 90:
            periodo = "⏰ Moderado (60-90d)"
        else:
            periodo = "📊 Crítico (>90d)"
        
        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "celular": cliente.celular,
            "email": cliente.email,
            "data_ultima_compra": cliente.data_ultima_compra.isoformat(),
            "valor_total_compras": cliente.valor_total_compras,
            "dias_sem_comprar": dias,
            "periodo": periodo,
            "vendedor_id": cliente.vendedor_id,
            "vendedor_anterior_id": cliente.vendedor_anterior_id,
            "contatado": cliente.contatado,
            "data_contato": cliente.data_contato.isoformat() if cliente.data_contato else None,
            "observacoes": cliente.observacoes,
            "prioridade": cliente.prioridade
        })
    
    resultado.sort(key=lambda x: x["dias_sem_comprar"])
    return resultado

@app.put("/api/clientes/{cliente_id}")
async def atualizar_cliente(cliente_id: int, dados: ClienteUpdate, db: Session = Depends(get_db)):
    """Atualiza atributos customizáveis do cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if dados.prioridade is not None:
        cliente.prioridade = max(0, min(10, dados.prioridade))
    if dados.observacoes is not None:
        cliente.observacoes = dados.observacoes
    
    db.commit()
    return {"message": "Cliente atualizado com sucesso"}

@app.post("/api/distribuir")
async def distribuir_clientes(config: DistribuicaoConfig, db: Session = Depends(get_db)):
    """
    Distribui clientes de forma inteligente baseado em atributos customizáveis
    PRIORIZA vendedor anterior quando possível!
    
    Parâmetros:
    - num_vendedores: Quantidade de vendedores (1-50)
    - atributo_peso: Atributo usado para ponderar distribuição
    - pesos_vendedores: Lista de pesos para cada vendedor
    - priorizar_vendedor_anterior: Se True, tenta alocar ao vendedor que já atendeu
    """
    if config.num_vendedores < 1 or config.num_vendedores > 50:
        raise HTTPException(status_code=400, detail="Número de vendedores deve estar entre 1 e 50")
    
    if len(config.pesos_vendedores) != config.num_vendedores:
        raise HTTPException(status_code=400, detail="Quantidade de pesos deve ser igual ao número de vendedores")
    
    if any(peso <= 0 for peso in config.pesos_vendedores):
        raise HTTPException(status_code=400, detail="Todos os pesos devem ser maiores que zero")
    
    # Atualizar configuração no banco
    config_db = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    if config_db:
        config_db.valor = str(config.num_vendedores)
    
    # Buscar clientes disponíveis (não contatados)
    clientes_disponiveis = db.query(Cliente).filter(
        Cliente.contatado == False
    ).all()
    
    if not clientes_disponiveis:
        return {"message": "Nenhum cliente disponível para distribuir", "distribuidos": 0}
    
    hoje = datetime.now()
    
    # Separar clientes COM e SEM vendedor anterior
    clientes_com_historico = [c for c in clientes_disponiveis if c.vendedor_anterior_id and c.vendedor_anterior_id <= config.num_vendedores]
    clientes_sem_historico = [c for c in clientes_disponiveis if not c.vendedor_anterior_id or c.vendedor_anterior_id > config.num_vendedores]
    
    # Ordenar ambos os grupos pelo critério escolhido
    def ordenar_clientes(clientes):
        if config.atributo_peso == "prioridade":
            return sorted(clientes, key=lambda c: c.prioridade, reverse=True)
        elif config.atributo_peso == "valor_total":
            return sorted(clientes, key=lambda c: c.valor_total_compras, reverse=True)
        elif config.atributo_peso == "dias_sem_comprar":
            return sorted(clientes, key=lambda c: (hoje - c.data_ultima_compra).days)
        elif config.atributo_peso == "vendedor_anterior":
            return sorted(clientes, key=lambda c: c.vendedor_anterior_id if c.vendedor_anterior_id else 999)
        else:
            result = clientes.copy()
            random.shuffle(result)
            return result
    
    clientes_com_historico = ordenar_clientes(clientes_com_historico)
    clientes_sem_historico = ordenar_clientes(clientes_sem_historico)
    
    # Determinar critério para exibição
    criterios = {
        "prioridade": "prioridade (maior primeiro)",
        "valor_total": "valor total de compras (maior primeiro)",
        "dias_sem_comprar": "dias sem comprar (mais urgente primeiro)",
        "vendedor_anterior": "vendedor anterior (priorizado)",
        "aleatorio": "aleatório"
    }
    criterio = criterios.get(config.atributo_peso, "personalizado")
    
    # Calcular capacidade de cada vendedor
    soma_pesos = sum(config.pesos_vendedores)
    total_clientes = len(clientes_disponiveis)
    
    capacidades = []
    clientes_distribuidos_calc = 0
    
    for i, peso in enumerate(config.pesos_vendedores):
        if i == len(config.pesos_vendedores) - 1:
            capacidade = total_clientes - clientes_distribuidos_calc
        else:
            capacidade = int((peso / soma_pesos) * total_clientes)
        
        capacidades.append({
            "vendedor_id": i + 1,
            "peso": peso,
            "capacidade": capacidade,
            "alocados": 0,
            "priorizados": 0  # Clientes que voltaram ao vendedor anterior
        })
        clientes_distribuidos_calc += capacidade
    
    # FASE 1: Distribuir clientes COM histórico, priorizando vendedor anterior
    if config.priorizar_vendedor_anterior:
        for cliente in clientes_com_historico:
            vendedor_anterior = cliente.vendedor_anterior_id
            vendedor_info = capacidades[vendedor_anterior - 1]
            
            # Se o vendedor ainda tem capacidade, aloca para ele
            if vendedor_info["alocados"] < vendedor_info["capacidade"]:
                cliente.vendedor_id = vendedor_anterior
                cliente.status = "atribuido"
                cliente.data_atribuicao = datetime.now()
                vendedor_info["alocados"] += 1
                vendedor_info["priorizados"] += 1
            else:
                # Senão, adiciona de volta à lista sem histórico
                clientes_sem_historico.append(cliente)
    else:
        # Se não priorizar, junta tudo
        clientes_sem_historico.extend(clientes_com_historico)
        clientes_sem_historico = ordenar_clientes(clientes_sem_historico)
    
    # FASE 2: Distribuir clientes restantes balanceadamente
    idx_vendedor = 0
    for cliente in clientes_sem_historico:
        # Encontrar próximo vendedor com capacidade
        tentativas = 0
        while tentativas < config.num_vendedores:
            vendedor_info = capacidades[idx_vendedor % config.num_vendedores]
            
            if vendedor_info["alocados"] < vendedor_info["capacidade"]:
                cliente.vendedor_id = vendedor_info["vendedor_id"]
                cliente.status = "atribuido"
                cliente.data_atribuicao = datetime.now()
                vendedor_info["alocados"] += 1
                idx_vendedor += 1
                break
            
            idx_vendedor += 1
            tentativas += 1
    
    db.commit()
    
    total_distribuido = sum(v["alocados"] for v in capacidades)
    total_priorizados = sum(v["priorizados"] for v in capacidades)
    
    return {
        "message": f"✅ {total_distribuido} cliente(s) distribuído(s) entre {config.num_vendedores} vendedor(es)",
        "criterio": criterio,
        "total_distribuido": total_distribuido,
        "priorizados": total_priorizados,
        "detalhes": [
            {
                "vendedor_id": v["vendedor_id"],
                "peso": v["peso"],
                "clientes_alocados": v["alocados"],
                "priorizados": v["priorizados"],
                "percentual": round((v["alocados"] / total_distribuido * 100) if total_distribuido > 0 else 0, 1)
            }
            for v in capacidades
        ]
    }

@app.post("/api/liberar-todos")
async def liberar_todos_clientes(db: Session = Depends(get_db)):
    """Libera todos os clientes (remove todas as atribuições)"""
    clientes = db.query(Cliente).filter(
        Cliente.vendedor_id.isnot(None),
        Cliente.contatado == False
    ).all()
    
    for cliente in clientes:
        cliente.vendedor_id = None
        cliente.status = "disponivel"
        cliente.data_atribuicao = None
    
    db.commit()
    return {"message": f"✅ {len(clientes)} cliente(s) liberado(s)", "total": len(clientes)}

@app.post("/api/marcar-contatado/{cliente_id}")
async def marcar_contatado(cliente_id: int, observacoes: str = None, db: Session = Depends(get_db)):
    """Marca cliente como contatado e salva vendedor atual como vendedor_anterior"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Salvar vendedor atual como vendedor anterior (histórico)
    if cliente.vendedor_id:
        cliente.vendedor_anterior_id = cliente.vendedor_id
    
    cliente.contatado = True
    cliente.status = "contatado"
    cliente.data_contato = datetime.now()
    if observacoes:
        cliente.observacoes = observacoes
    
    db.commit()
    return {"message": "Cliente marcado como contatado", "vendedor_anterior_salvo": cliente.vendedor_anterior_id}

@app.get("/api/exportar/vendedor/{vendedor_id}")
async def exportar_clientes_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """Exporta lista formatada de clientes de um vendedor específico"""
    clientes = db.query(Cliente).filter(
        Cliente.vendedor_id == vendedor_id,
        Cliente.contatado == False
    ).all()
    
    hoje = datetime.now()
    
    # Ordenar por urgência
    clientes_ordenados = sorted(
        clientes,
        key=lambda c: (hoje - c.data_ultima_compra).days
    )
    
    # Formato texto enriquecido
    texto = "═" * 60 + "\n"
    texto += f"  CLIENTES PARA: VENDEDOR #{vendedor_id}\n"
    texto += f"  Data/Hora: {hoje.strftime('%d/%m/%Y às %H:%M:%S')}\n"
    texto += "═" * 60 + "\n\n"
    
    if not clientes_ordenados:
        texto += "⚠️  Nenhum cliente pendente para este vendedor.\n"
    else:
        for i, cliente in enumerate(clientes_ordenados, 1):
            dias = (hoje - cliente.data_ultima_compra).days
            
            # Badge de urgência
            if 30 <= dias <= 45:
                urgencia = "🔥 URGENTE"
            elif 45 < dias <= 60:
                urgencia = "⚠️ ATENÇÃO"
            elif 60 < dias <= 90:
                urgencia = "⏰ MODERADO"
            else:
                urgencia = "📊 CRÍTICO"
            
            texto += f"{'─' * 60}\n"
            texto += f"#{i:03d} - {cliente.nome.upper()} {urgencia}\n"
            texto += f"{'─' * 60}\n"
            texto += f"📱 Celular:      {cliente.celular}\n"
            texto += f"📧 Email:        {cliente.email}\n"
            texto += f"⏱️  Sem comprar:  {dias} dias\n"
            texto += f"💰 Total gasto:  R$ {cliente.valor_total_compras:,.2f}\n"
            texto += f"⭐ Prioridade:   {cliente.prioridade}/10\n"
            texto += f"🗓️  Última compra: {cliente.data_ultima_compra.strftime('%d/%m/%Y')}\n"
            
            if cliente.vendedor_anterior_id:
                texto += f"🔄 Já atendido por: Vendedor #{cliente.vendedor_anterior_id}\n"
            
            if cliente.observacoes:
                texto += f"📝 Obs: {cliente.observacoes}\n"
            
            texto += "\n"
    
    texto += "═" * 60 + "\n"
    texto += f"TOTAL: {len(clientes_ordenados)} cliente(s)\n"
    texto += "═" * 60 + "\n"
    
    return {"texto": texto, "total": len(clientes_ordenados)}

@app.get("/api/exportar/todos")
async def exportar_todos_vendedores(db: Session = Depends(get_db)):
    """Exporta lista de TODOS os vendedores com seus respectivos clientes"""
    # Buscar número de vendedores configurado
    config_db = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    
    num_vendedores = int(config_db.valor) if config_db else 5
    hoje = datetime.now()
    
    texto_completo = "═" * 80 + "\n"
    texto_completo += "  EXPORTAÇÃO COMPLETA - TODOS OS VENDEDORES\n"
    texto_completo += f"  Data/Hora: {hoje.strftime('%d/%m/%Y às %H:%M:%S')}\n"
    texto_completo += "═" * 80 + "\n\n"
    
    total_geral = 0
    
    for vendedor_id in range(1, num_vendedores + 1):
        clientes = db.query(Cliente).filter(
            Cliente.vendedor_id == vendedor_id,
            Cliente.contatado == False
        ).all()
        
        clientes_ordenados = sorted(
            clientes,
            key=lambda c: (hoje - c.data_ultima_compra).days
        )
        
        texto_completo += "\n" + "█" * 80 + "\n"
        texto_completo += f"█  VENDEDOR #{vendedor_id} - {len(clientes_ordenados)} CLIENTE(S)\n"
        texto_completo += "█" * 80 + "\n\n"
        
        if not clientes_ordenados:
            texto_completo += "⚠️  Nenhum cliente pendente para este vendedor.\n\n"
        else:
            for i, cliente in enumerate(clientes_ordenados, 1):
                dias = (hoje - cliente.data_ultima_compra).days
                
                if 30 <= dias <= 45:
                    urgencia = "🔥 URGENTE"
                elif 45 < dias <= 60:
                    urgencia = "⚠️ ATENÇÃO"
                elif 60 < dias <= 90:
                    urgencia = "⏰ MODERADO"
                else:
                    urgencia = "📊 CRÍTICO"
                
                texto_completo += f"  {i}. {cliente.nome} - {urgencia}\n"
                texto_completo += f"     📱 {cliente.celular} | 📧 {cliente.email}\n"
                texto_completo += f"     ⏱️  {dias} dias | 💰 R$ {cliente.valor_total_compras:,.2f} | ⭐ Prior: {cliente.prioridade}/10\n"
                if cliente.vendedor_anterior_id:
                    texto_completo += f"     🔄 Já atendido por: Vendedor #{cliente.vendedor_anterior_id}\n"
                if cliente.observacoes:
                    texto_completo += f"     📝 {cliente.observacoes}\n"
                texto_completo += "\n"
            
            total_geral += len(clientes_ordenados)
    
    texto_completo += "\n" + "═" * 80 + "\n"
    texto_completo += f"TOTAL GERAL: {total_geral} cliente(s) em {num_vendedores} vendedor(es)\n"
    texto_completo += "═" * 80 + "\n"
    
    return {"texto": texto_completo, "total": total_geral, "vendedores": num_vendedores}

@app.get("/api/status-vendedores")
async def status_vendedores(db: Session = Depends(get_db)):
    """Retorna status de cada vendedor (quantos clientes pendentes, se está livre, etc)"""
    config_db = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    num_vendedores = int(config_db.valor) if config_db else 5
    
    status_list = []
    for vid in range(1, num_vendedores + 1):
        pendentes = db.query(Cliente).filter(
            Cliente.vendedor_id == vid,
            Cliente.contatado == False
        ).count()
        
        contatados = db.query(Cliente).filter(
            Cliente.vendedor_id == vid,
            Cliente.contatado == True
        ).count()
        
        total = pendentes + contatados
        
        # Vendedor está "livre" se não tem clientes pendentes
        livre = (pendentes == 0)
        
        status_list.append({
            "vendedor_id": vid,
            "pendentes": pendentes,
            "contatados": contatados,
            "total": total,
            "livre": livre,
            "status": "🟢 Livre" if livre else f"🔴 {pendentes} pendente(s)"
        })
    
    # Contar vendedores livres e sobrecarregados
    livres = [v for v in status_list if v["livre"]]
    ocupados = [v for v in status_list if not v["livre"]]
    
    # Identificar necessidade de rebalanceamento
    precisa_rebalancear = False
    if livres and ocupados:
        # Se tem vendedor livre E tem vendedor com clientes, pode rebalancear
        precisa_rebalancear = True
    
    return {
        "vendedores": status_list,
        "total_vendedores": num_vendedores,
        "vendedores_livres": len(livres),
        "vendedores_ocupados": len(ocupados),
        "precisa_rebalancear": precisa_rebalancear,
        "recomendacao": "✅ Clique em 'Rebalancear Automaticamente' para redistribuir" if precisa_rebalancear else "✅ Sistema balanceado"
    }

@app.post("/api/rebalancear-automatico")
async def rebalancear_automatico(db: Session = Depends(get_db)):
    """
    Rebalanceamento inteligente:
    - Identifica vendedores livres (sem clientes pendentes)
    - Redistribui clientes pendentes entre TODOS os vendedores
    - Prioriza vendedor anterior quando possível
    """
    config_db = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    num_vendedores = int(config_db.valor) if config_db else 5
    
    # Buscar clientes pendentes (não contatados)
    clientes_pendentes = db.query(Cliente).filter(
        Cliente.contatado == False,
        Cliente.vendedor_id.isnot(None)
    ).all()
    
    if not clientes_pendentes:
        return {
            "message": "Nenhum cliente pendente para rebalancear",
            "redistribuidos": 0
        }
    
    # Verificar status de cada vendedor
    vendedores_status = []
    for vid in range(1, num_vendedores + 1):
        pendentes = db.query(Cliente).filter(
            Cliente.vendedor_id == vid,
            Cliente.contatado == False
        ).count()
        vendedores_status.append({
            "vendedor_id": vid,
            "pendentes": pendentes,
            "livre": (pendentes == 0)
        })
    
    vendedores_livres = [v["vendedor_id"] for v in vendedores_status if v["livre"]]
    
    if not vendedores_livres:
        return {
            "message": "Nenhum vendedor livre no momento. Todos ainda têm clientes pendentes.",
            "redistribuidos": 0,
            "dica": "Marque clientes como contatados para liberar vendedores"
        }
    
    # Liberar TODOS os clientes pendentes
    for cliente in clientes_pendentes:
        cliente.vendedor_id = None
        cliente.status = "disponivel"
        cliente.data_atribuicao = None
    
    db.commit()
    
    # Redistribuir com pesos iguais entre TODOS os vendedores
    pesos = [1.0] * num_vendedores
    
    config = DistribuicaoConfig(
        num_vendedores=num_vendedores,
        atributo_peso="dias_sem_comprar",  # Priorizar urgência
        pesos_vendedores=pesos,
        priorizar_vendedor_anterior=True  # Sempre priorizar histórico
    )
    
    resultado = await distribuir_clientes(config, db)
    
    return {
        "message": f"🔄 Rebalanceamento automático concluído!",
        "vendedores_livres_encontrados": len(vendedores_livres),
        "vendedores_que_estavam_livres": vendedores_livres,
        "redistribuidos": resultado["total_distribuido"],
        "priorizados": resultado.get("priorizados", 0),
        "detalhes": resultado["detalhes"]
    }

@app.get("/api/estatisticas")
async def estatisticas(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais do sistema"""
    hoje = datetime.now()
    
    # Buscar número de vendedores
    config_db = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    num_vendedores = int(config_db.valor) if config_db else 5
    
    total = db.query(Cliente).count()
    disponiveis = db.query(Cliente).filter(Cliente.vendedor_id.is_(None), Cliente.contatado == False).count()
    atribuidos = db.query(Cliente).filter(Cliente.vendedor_id.isnot(None), Cliente.contatado == False).count()
    contatados = db.query(Cliente).filter(Cliente.contatado == True).count()
    
    # Estatísticas por vendedor
    stats_vendedores = []
    for vid in range(1, num_vendedores + 1):
        total_vendedor = db.query(Cliente).filter(Cliente.vendedor_id == vid).count()
        pendentes = db.query(Cliente).filter(
            Cliente.vendedor_id == vid,
            Cliente.contatado == False
        ).count()
        contatados_vendedor = db.query(Cliente).filter(
            Cliente.vendedor_id == vid,
            Cliente.contatado == True
        ).count()
        
        # Não precisa mais calcular potencial (campo removido)
        
        stats_vendedores.append({
            "vendedor_id": vid,
            "total": total_vendedor,
            "pendentes": pendentes,
            "contatados": contatados_vendedor,
            "taxa_conversao": round((contatados_vendedor / total_vendedor * 100) if total_vendedor > 0 else 0, 1)
        })
    
    # Médias dos atributos customizáveis
    clientes_disponiveis = db.query(Cliente).filter(Cliente.contatado == False).all()
    if clientes_disponiveis:
        media_prioridade = sum(c.prioridade for c in clientes_disponiveis) / len(clientes_disponiveis)
    else:
        media_prioridade = 0
    
    return {
        "total_clientes": total,
        "disponiveis": disponiveis,
        "atribuidos": atribuidos,
        "contatados": contatados,
        "num_vendedores": num_vendedores,
        "vendedores": stats_vendedores,
        "medias": {
            "prioridade": round(media_prioridade, 2)
        }
    }

@app.get("/api/config/vendedores")
async def obter_num_vendedores(db: Session = Depends(get_db)):
    """Retorna número atual de vendedores configurado"""
    config = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    return {"num_vendedores": int(config.valor) if config else 5}

@app.post("/api/config/vendedores/{num}")
async def configurar_vendedores(num: int, db: Session = Depends(get_db)):
    """Configura número de vendedores"""
    if num < 1 or num > 50:
        raise HTTPException(status_code=400, detail="Número deve estar entre 1 e 50")
    
    config = db.query(ConfiguracaoSistema).filter(
        ConfiguracaoSistema.chave == "num_vendedores"
    ).first()
    
    if config:
        config.valor = str(num)
    else:
        config = ConfiguracaoSistema(
            chave="num_vendedores",
            valor=str(num),
            descricao="Número de vendedores ativos"
        )
        db.add(config)
    
    db.commit()
    return {"message": f"Configurado para {num} vendedores", "num_vendedores": num}

# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
