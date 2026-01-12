"""
CRM Kanban v3.0 - Sistema Simplificado APENAS ADMIN
Sistema focado em gestão de clientes para exportação manual aos vendedores
"""
import random
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List

from faker import Faker
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

# ==================== DATABASE ====================
DATABASE_URL = "sqlite:///./crm_kanban.db"
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
    vendedor_atribuido = Column(String, nullable=True)
    data_atribuicao = Column(DateTime, nullable=True)
    contatado = Column(Boolean, default=False)
    data_contato = Column(DateTime, nullable=True)
    observacoes = Column(String, nullable=True)

class Vendedor(Base):
    __tablename__ = "vendedores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    
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
    vendedor_atribuido: str | None
    contatado: bool
    observacoes: str | None

class AtribuirRequest(BaseModel):
    cliente_ids: List[int]
    vendedor_nome: str

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
    
    # Criar vendedores
    nomes_vendedores = ["João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa", "Carlos Ferreira"]
    for nome in nomes_vendedores:
        vendedor = Vendedor(nome=nome)
        db.add(vendedor)
    
    # Criar clientes
    periodos = [
        (30, 45, 30),   # Urgente: 30 clientes
        (45, 60, 25),   # Atenção: 25 clientes
        (60, 90, 20),   # Moderado: 20 clientes
        (90, 180, 15),  # Crítico: 15 clientes
        (0, 30, 20),    # Ativos: 20 clientes
    ]
    
    ddds = ['11', '21', '31', '41', '51', '61', '71', '81', '85', '91']
    
    for dias_min, dias_max, quantidade in periodos:
        for _ in range(quantidade):
            dias_atras = random.randint(dias_min, dias_max)
            data_compra = hoje - timedelta(days=dias_atras)
            
            ddd = random.choice(ddds)
            numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            celular = f"({ddd}) {numero}"
            
            cliente = Cliente(
                nome=fake.name(),
                celular=celular,
                email=fake.email(),
                data_ultima_compra=data_compra,
                valor_total_compras=round(random.uniform(500, 15000), 2),
                status="disponivel"
            )
            db.add(cliente)
    
    db.commit()
    print(f"✅ Banco populado: 110 clientes, 5 vendedores, 1 admin")

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
    title="CRM Kanban v3.0",
    description="Sistema simplificado de gestão de clientes (apenas admin)",
    version="3.0.0",
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
    return FileResponse("static/admin_v3.html")

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
    """Lista todos os clientes com informações de período"""
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
            "vendedor_atribuido": cliente.vendedor_atribuido,
            "contatado": cliente.contatado,
            "data_contato": cliente.data_contato.isoformat() if cliente.data_contato else None,
            "observacoes": cliente.observacoes
        })
    
    # Ordenar por dias sem comprar (decrescente)
    resultado.sort(key=lambda x: x["dias_sem_comprar"], reverse=False)
    return resultado

@app.get("/api/vendedores")
async def listar_vendedores(db: Session = Depends(get_db)):
    """Lista todos os vendedores"""
    vendedores = db.query(Vendedor).all()
    return [{"id": v.id, "nome": v.nome} for v in vendedores]

@app.post("/api/atribuir")
async def atribuir_clientes(atribuicao: AtribuirRequest, db: Session = Depends(get_db)):
    """Atribui clientes a um vendedor de forma inteligente"""
    # Verificar se vendedor existe
    vendedor = db.query(Vendedor).filter(Vendedor.nome == atribuicao.vendedor_nome).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    # Atribuir clientes
    clientes_atualizados = 0
    clientes_ja_atribuidos = []
    
    for cliente_id in atribuicao.cliente_ids:
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            # Verificar se já está atribuído a outro vendedor
            if cliente.vendedor_atribuido and cliente.vendedor_atribuido != atribuicao.vendedor_nome and not cliente.contatado:
                clientes_ja_atribuidos.append(cliente.nome)
                continue
            
            cliente.vendedor_atribuido = atribuicao.vendedor_nome
            cliente.status = "atribuido"
            cliente.data_atribuicao = datetime.now()
            clientes_atualizados += 1
    
    db.commit()
    
    mensagem = f"✅ {clientes_atualizados} cliente(s) atribuído(s) a {atribuicao.vendedor_nome}"
    if clientes_ja_atribuidos:
        mensagem += f"\n⚠️ {len(clientes_ja_atribuidos)} cliente(s) já atribuído(s) a outros vendedores (ignorados)"
    
    return {"message": mensagem, "atribuidos": clientes_atualizados, "ignorados": len(clientes_ja_atribuidos)}

@app.post("/api/liberar/{cliente_id}")
async def liberar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Libera um cliente (remove atribuição)"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente.vendedor_atribuido = None
    cliente.status = "disponivel"
    cliente.data_atribuicao = None
    db.commit()
    
    return {"message": "Cliente liberado com sucesso"}

@app.post("/api/marcar-contatado/{cliente_id}")
async def marcar_contatado(cliente_id: int, observacoes: str = None, db: Session = Depends(get_db)):
    """Marca cliente como contatado"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente.contatado = True
    cliente.status = "contatado"
    cliente.data_contato = datetime.now()
    if observacoes:
        cliente.observacoes = observacoes
    
    db.commit()
    return {"message": "Cliente marcado como contatado"}

@app.post("/api/redistribuir-automatico")
async def redistribuir_automatico(db: Session = Depends(get_db)):
    """Redistribui automaticamente clientes disponíveis entre vendedores de forma inteligente"""
    # Buscar vendedores
    vendedores = db.query(Vendedor).all()
    if not vendedores:
        raise HTTPException(status_code=400, detail="Nenhum vendedor cadastrado")
    
    # Buscar clientes disponíveis (não atribuídos e não contatados)
    clientes_disponiveis = db.query(Cliente).filter(
        Cliente.status == "disponivel",
        Cliente.contatado == False
    ).all()
    
    if not clientes_disponiveis:
        return {"message": "Nenhum cliente disponível para distribuir", "distribuidos": 0}
    
    # Calcular carga atual de cada vendedor
    carga_vendedores = []
    for v in vendedores:
        pendentes = db.query(Cliente).filter(
            Cliente.vendedor_atribuido == v.nome,
            Cliente.contatado == False
        ).count()
        carga_vendedores.append({"vendedor": v, "carga": pendentes})
    
    # Ordenar por carga (menor carga primeiro)
    carga_vendedores.sort(key=lambda x: x["carga"])
    
    # Ordenar clientes por urgência (30-45 dias primeiro)
    hoje = datetime.now()
    clientes_ordenados = sorted(
        clientes_disponiveis,
        key=lambda c: (hoje - c.data_ultima_compra).days,
        reverse=False
    )
    
    # Distribuir de forma balanceada
    distribuidos = 0
    idx_vendedor = 0
    
    for cliente in clientes_ordenados:
        vendedor_atual = carga_vendedores[idx_vendedor % len(carga_vendedores)]
        
        cliente.vendedor_atribuido = vendedor_atual["vendedor"].nome
        cliente.status = "atribuido"
        cliente.data_atribuicao = datetime.now()
        
        vendedor_atual["carga"] += 1
        distribuidos += 1
        idx_vendedor += 1
        
        # Re-ordenar para manter balanceamento
        if idx_vendedor % len(vendedores) == 0:
            carga_vendedores.sort(key=lambda x: x["carga"])
    
    db.commit()
    
    # Preparar detalhes da distribuição
    detalhes = []
    for item in carga_vendedores:
        detalhes.append({
            "vendedor": item["vendedor"].nome,
            "clientes": item["carga"]
        })
    
    return {
        "message": f"✅ {distribuidos} cliente(s) distribuído(s) automaticamente entre {len(vendedores)} vendedor(es)",
        "distribuidos": distribuidos,
        "vendedores": len(vendedores),
        "detalhes": detalhes
    }

@app.get("/api/estatisticas")
async def estatisticas(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais"""
    hoje = datetime.now()
    
    total = db.query(Cliente).count()
    disponiveis = db.query(Cliente).filter(Cliente.status == "disponivel").count()
    atribuidos = db.query(Cliente).filter(Cliente.status == "atribuido").count()
    contatados = db.query(Cliente).filter(Cliente.status == "contatado").count()
    
    # Por vendedor
    vendedores = db.query(Vendedor).all()
    stats_vendedores = []
    for v in vendedores:
        total_vendedor = db.query(Cliente).filter(Cliente.vendedor_atribuido == v.nome).count()
        contatados_vendedor = db.query(Cliente).filter(
            Cliente.vendedor_atribuido == v.nome,
            Cliente.contatado == True
        ).count()
        pendentes_vendedor = total_vendedor - contatados_vendedor
        
        stats_vendedores.append({
            "nome": v.nome,
            "total": total_vendedor,
            "pendentes": pendentes_vendedor,
            "contatados": contatados_vendedor,
            "taxa_conversao": round((contatados_vendedor / total_vendedor * 100) if total_vendedor > 0 else 0, 1)
        })
    
    return {
        "total_clientes": total,
        "disponiveis": disponiveis,
        "atribuidos": atribuidos,
        "contatados": contatados,
        "vendedores": stats_vendedores
    }

@app.get("/api/exportar/{vendedor_nome}")
async def exportar_vendedor(vendedor_nome: str, db: Session = Depends(get_db)):
    """Exporta lista de clientes de um vendedor para copiar e colar"""
    clientes = db.query(Cliente).filter(
        Cliente.vendedor_atribuido == vendedor_nome,
        Cliente.contatado == False
    ).all()
    
    hoje = datetime.now()
    
    # Ordenar por urgência (30-45 dias primeiro)
    clientes_ordenados = sorted(
        clientes,
        key=lambda c: (hoje - c.data_ultima_compra).days
    )
    
    # Formato texto simples para copiar e colar
    texto = f"═══════════════════════════════════════════════\n"
    texto += f"    CLIENTES PARA: {vendedor_nome.upper()}\n"
    texto += f"    Data: {hoje.strftime('%d/%m/%Y %H:%M')}\n"
    texto += f"═══════════════════════════════════════════════\n\n"
    
    if not clientes_ordenados:
        texto += "Nenhum cliente pendente.\n"
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
            
            texto += f"{i}. {cliente.nome} - {urgencia}\n"
            texto += f"   📱 {cliente.celular}\n"
            texto += f"   📧 {cliente.email}\n"
            texto += f"   📊 Sem comprar há {dias} dias\n"
            texto += f"   💰 Total compras: R$ {cliente.valor_total_compras:,.2f}\n"
            texto += f"   🗓️  Última compra: {cliente.data_ultima_compra.strftime('%d/%m/%Y')}\n"
            texto += f"   ─────────────────────────────────────────\n\n"
    
    texto += f"\nTotal: {len(clientes_ordenados)} cliente(s)\n"
    texto += f"═══════════════════════════════════════════════\n"
    
    return JSONResponse(content={"texto": texto, "total": len(clientes_ordenados)})

# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
