# 📊 Arquitetura do Sistema CRM Kanban v2.0

## 🏗️ Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CRM KANBAN v2.0                          │
│                  Sistema de Gestão de Clientes                  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            ┌───────▼────────┐         ┌────────▼───────┐
            │   FRONTEND     │         │    BACKEND     │
            │   (Static)     │◄────────┤   (FastAPI)    │
            └────────────────┘         └────────────────┘
                                               │
                        ┌──────────────────────┼──────────────────────┐
                        │                      │                      │
                  ┌─────▼─────┐        ┌──────▼──────┐       ┌──────▼──────┐
                  │  Database │        │  WebSocket  │       │   Routes    │
                  │  (SQLite) │        │   Manager   │       │   (APIs)    │
                  └───────────┘        └─────────────┘       └─────────────┘
```

---

## 📁 Estrutura de Diretórios

### Backend Modular

```
backend/
├── database.py          → Configuração SQLAlchemy + SessionLocal
├── websocket.py         → ConnectionManager para tempo real
│
├── models/
│   ├── models.py        → Entidades do banco (Vendedor, Cliente, etc)
│   └── schemas.py       → Schemas Pydantic para validação
│
├── routes/
│   ├── auth.py          → Login/Logout (/api/auth/*)
│   ├── vendedor.py      → Endpoints vendedor (/api/vendedor/*)
│   └── admin.py         → Endpoints admin (/api/admin/*)
│
└── utils/
    ├── distribuicao.py  → Lógica de redistribuição de clientes
    └── populate.py      → População do banco com dados fictícios
```

### Frontend Organizado

```
static/
├── index.html           → Interface do Vendedor
├── script.js            → Lógica do Vendedor
├── styles.css           → Estilos Comuns
│
├── admin.html           → Interface do Admin
├── admin-script.js      → Lógica do Admin
└── admin-styles.css     → Estilos Admin
```

---

## 🔄 Fluxo de Dados

### 1. Autenticação

```
┌──────────┐     POST /api/auth/login     ┌──────────┐
│ Frontend │ ─────────────────────────────→│ Backend  │
│          │                               │          │
│          │ ◄─────────────────────────────│          │
└──────────┘   {id, nome, is_admin}        └──────────┘
                                                 │
                                                 ▼
                                    ┌────────────────────┐
                                    │ Set online = True  │
                                    │ Redistribuir()     │
                                    └────────────────────┘
```

### 2. Distribuição de Clientes (Corrigido)

```
┌─────────────────────────────────────────────────────────────┐
│              LÓGICA DE DISTRIBUIÇÃO v2.0                    │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
     ┌──────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
     │  Buscar     │ │  Limpar     │ │ Distribuir │
     │  Clientes   │ │ Atribuições │ │ Round-Robin│
     │  30-60 dias │ │  Offline    │ │  Vendedores│
     └─────────────┘ └─────────────┘ └────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                     ┌──────▼──────┐
                     │   Commit    │
                     │   Database  │
                     └─────────────┘
```

### 3. Comunicação Tempo Real

```
┌──────────┐                              ┌──────────┐
│Vendedor 1│ ──┐                      ┌──▶│Vendedor 2│
└──────────┘   │                      │   └──────────┘
               │   ┌──────────────┐   │
               ├──▶│  WebSocket   │───┤
               │   │   Manager    │   │
               │   └──────────────┘   │
               │                      │   ┌──────────┐
               └──────────────────────┴──▶│  Admin   │
                                          └──────────┘
       Eventos:
       • cliente_contatado
       • vendedor_online
       • redistribuicao_completa
```

---

## 🗄️ Modelo de Dados

### Diagrama ER Simplificado

```
┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
│   Vendedor   │         │ ClienteVendedor │         │   Cliente    │
├──────────────┤         ├─────────────────┤         ├──────────────┤
│ id (PK)      │◄────────│ vendedor_id(FK) │         │ id (PK)      │
│ nome         │         │ cliente_id (FK) │────────▶│ nome         │
│ senha        │         │ contatado       │         │ celular      │
│ online       │         │ data_atribuicao │         │ email        │
│ is_admin     │         │ observacoes     │         │ data_ultima  │
└──────────────┘         └─────────────────┘         │ valor_total  │
                                                      │ status       │
                                                      └──────────────┘
                                                             │
                                                             │
                         ┌──────────────┐                   │
                         │    Pedido    │                   │
                         ├──────────────┤                   │
                         │ id (PK)      │                   │
                         │ cliente_id◄──┼───────────────────┘
                         │ produto_id   │
                         │ data_pedido  │
                         │ valor        │
                         └──────────────┘
```

### Estados do Cliente

```
┌─────────────┐
│ disponivel  │  → Cliente livre para atribuição
└─────────────┘
       │
       ▼
┌─────────────┐
│  atribuido  │  → Cliente designado a vendedor
└─────────────┘
       │
       ▼
┌─────────────┐
│  contatado  │  → Cliente já foi abordado
└─────────────┘

Estados especiais:
• ativo    → Comprou recentemente (<30 dias)
• inativo  → Muito tempo sem comprar (>60 dias)
```

---

## 🎯 Endpoints por Perfil

### Vendedor Endpoints

```
┌────────────────────────────────────────────────────────┐
│              VENDEDOR API (/api/vendedor)              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  GET /meus-clientes/{id}                              │
│  ├─ Retorna: Lista de clientes atribuídos            │
│  └─ Inclui: dias_sem_comprar, dados completos        │
│                                                        │
│  POST /marcar-contatado/{id}                          │
│  ├─ Body: {cliente_id, observacoes}                  │
│  ├─ Ação: Marca cliente como contatado               │
│  └─ Broadcast: Notifica via WebSocket                │
│                                                        │
│  GET /estatisticas/{id}                               │
│  ├─ Retorna: total_atribuidos, contatados            │
│  └─ Calcula: total_pendentes                         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Admin Endpoints

```
┌────────────────────────────────────────────────────────┐
│                ADMIN API (/api/admin)                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  GET /clientes-por-periodo                            │
│  ├─ Retorna: Clientes agrupados por período          │
│  └─ Períodos: 30-45d, 45-60d, 60-90d, >90d          │
│                                                        │
│  GET /todos-clientes                                  │
│  ├─ Retorna: Lista completa com status               │
│  └─ Inclui: vendedor_atribuido, dias_sem_comprar    │
│                                                        │
│  POST /realocar-cliente                               │
│  ├─ Body: {cliente_id, vendedor_id}                  │
│  ├─ Ação: Remove atribuição anterior                 │
│  └─ Cria: Nova atribuição para vendedor              │
│                                                        │
│  POST /redistribuir-todos                             │
│  ├─ Ação: Limpa TODAS atribuições não contatadas    │
│  ├─ Reset: Marca clientes como disponíveis           │
│  └─ Executa: redistribuir_clientes()                 │
│                                                        │
│  POST /liberar-cliente/{id}                           │
│  ├─ Ação: Remove atribuição do cliente               │
│  └─ Status: Volta para disponível                    │
│                                                        │
│  GET /estatisticas-gerais                             │
│  ├─ Retorna: Métricas completas do sistema          │
│  └─ Inclui: Performance por vendedor                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🔐 Camadas de Segurança

### Autenticação

```
┌────────────────────────────────────────┐
│         Fluxo de Autenticação          │
└────────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │   Login     │  → Valida nome + senha
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Verifica   │  → is_admin?
    │   Perfil    │
    └──────┬──────┘
           │
      ┌────┴────┐
      │         │
  ┌───▼──┐  ┌──▼───┐
  │Admin │  │Vend  │  → Define rotas permitidas
  └──────┘  └──────┘
```

### Validação de Dados

```
Request → Pydantic Schema → Validation → Business Logic
            │                    │
            └─ Fail ─────────────┴─→ HTTP 422
```

---

## 📈 Performance e Otimizações

### Database Queries

```python
# ✅ OTIMIZADO - Uma query com join
clientes = db.query(ClienteVendedor).join(Cliente).filter(...)

# ❌ NÃO OTIMIZADO - N+1 queries
for atrib in atribuicoes:
    cliente = db.query(Cliente).get(atrib.cliente_id)  # N queries!
```

### Índices Importantes

```sql
CREATE INDEX idx_cliente_data ON clientes(data_ultima_compra);
CREATE INDEX idx_vendedor_online ON vendedores(online);
CREATE INDEX idx_atribuicao_vendedor ON cliente_vendedor(vendedor_id);
CREATE INDEX idx_atribuicao_contatado ON cliente_vendedor(contatado);
```

---

## 🧪 Testes Recomendados

### Casos de Teste Críticos

1. **Distribuição com 1 Vendedor**
   - Todos os clientes vão para ele
   
2. **Distribuição com 3 Vendedores**
   - Divisão 18-18-19 (55 clientes)
   
3. **Vendedor Sai (Logout)**
   - Clientes são redistribuídos
   
4. **Cliente Contatado**
   - Não volta para redistribuição
   
5. **Admin Realoca**
   - Cliente vai para vendedor específico

---

## 🚀 Deploy para Produção

### Checklist

- [ ] Trocar SQLite por PostgreSQL
- [ ] Implementar hash de senhas (bcrypt)
- [ ] Adicionar JWT authentication
- [ ] Configurar HTTPS
- [ ] Rate limiting (ex: 100 req/min)
- [ ] Logs estruturados (JSON)
- [ ] Monitoring (Prometheus)
- [ ] Backup automático do banco
- [ ] Docker container
- [ ] CI/CD pipeline

### Exemplo Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

**Sistema v2.0 - Arquitetura Profissional e Escalável** 🚀
