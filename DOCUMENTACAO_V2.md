# 🎯 CRM Kanban v2.0 - Documentação Completa

## 🚀 O que há de novo na v2.0

### ✨ Melhorias Principais

1. **🐛 Bug Crítico Corrigido**: Sistema de distribuição agora funciona corretamente
   - Clientes são redistribuídos adequadamente entre vendedores
   - Status dos clientes gerenciado corretamente
   - Contadores de clientes pendentes funcionando

2. **👑 Painel de Administrador**: Interface completa para gestão
   - Visualização por períodos (30-45d, 45-60d, 60-90d, >90d)
   - Realocação manual de clientes
   - Estatísticas em tempo real
   - Performance dos vendedores

3. **📁 Arquitetura Reorganizada**: Código modular e escalável
   - Backend separado em módulos
   - Rotas organizadas por funcionalidade
   - Fácil manutenção e extensão

4. **🎨 Interface Melhorada**: UX aprimorada
   - Badges de urgência por período
   - Melhor organização visual
   - Responsiva e moderna

---

## 📋 Estrutura do Projeto

```
kanban-crm/
├── app.py                      # Aplicação principal FastAPI
├── backend/
│   ├── database.py             # Configuração do banco
│   ├── websocket.py            # Gerenciador WebSocket
│   ├── models/
│   │   ├── models.py           # Modelos SQLAlchemy
│   │   └── schemas.py          # Schemas Pydantic
│   ├── routes/
│   │   ├── auth.py             # Autenticação
│   │   ├── vendedor.py         # Endpoints vendedor
│   │   └── admin.py            # Endpoints admin
│   └── utils/
│       ├── distribuicao.py     # Lógica de distribuição
│       └── populate.py         # Popular banco
├── static/
│   ├── index.html              # Interface vendedor
│   ├── script.js               # Lógica vendedor
│   ├── admin.html              # Interface admin
│   ├── admin-script.js         # Lógica admin
│   ├── styles.css              # Estilos comuns
│   └── admin-styles.css        # Estilos admin
├── requirements.txt
├── README.md
└── GUIA_RAPIDO.md
```

---

## 🔧 Instalação e Uso

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python app.py

# OU usar o script
./start.sh
```

### Acessos

**Vendedores:**
- URL: http://localhost:8000
- Usuários: João Silva, Maria Santos, Pedro Oliveira, Ana Costa, Carlos Ferreira
- Senha: `123456`

**Administrador:**
- URL: http://localhost:8000 (redireciona automaticamente)
- Usuário: Admin
- Senha: `admin123`

---

## 🎯 Funcionalidades

### Para Vendedores

#### Dashboard
- ✅ **Estatísticas Pessoais**: Pendentes, Contatados, Total
- ✅ **Lista de Clientes**: Ordenada por urgência
- ✅ **Badges Inteligentes**: 
  - 🔥 Urgente (30-45 dias)
  - ⚠️ Atenção (45-60 dias)
- ✅ **Busca em Tempo Real**: Por nome, telefone ou email
- ✅ **Marcar Contato**: Com observações

#### Redistribuição Automática
- Clientes redistribuídos ao fazer login
- Clientes liberados ao fazer logout
- Atualização em tempo real via WebSocket

### Para Administradores

#### Visão Geral
- 📊 **Estatísticas Gerais**: Total de clientes, por status, por período
- 👥 **Vendedores Online**: Quantidade em tempo real

#### Clientes por Período
Organização em 4 categorias:
1. **🔥 Urgente (30-45 dias)**: Prioridade máxima
2. **⚠️ Atenção (45-60 dias)**: Prioridade alta
3. **⏰ Moderado (60-90 dias)**: Acompanhamento
4. **📊 Crítico (>90 dias)**: Clientes frios

#### Gestão de Clientes
- 📋 **Tabela Completa**: Todos os clientes com filtros
- 🔄 **Realocação Manual**: Atribuir cliente a vendedor específico
- 🔓 **Liberar Cliente**: Disponibilizar para redistribuição
- 🔄 **Redistribuir Todos**: Reset completo da distribuição

#### Performance dos Vendedores
- Total de clientes atribuídos
- Total de clientes contatados
- Taxa de conversão (%)
- Status online/offline

---

## 🔍 Como Funciona

### Sistema de Distribuição (Corrigido)

#### Identificação de Clientes Elegíveis
```python
# Clientes entre 30-60 dias sem comprar
hoje = datetime.now()
data_inicio = hoje - timedelta(days=60)
data_fim = hoje - timedelta(days=30)

clientes_elegiveis = Cliente.filter(
    data_ultima_compra >= data_inicio,
    data_ultima_compra <= data_fim,
    status != "contatado"
)
```

#### Distribuição Inteligente
1. **Vendedores Online**: Apenas vendedores ativos recebem clientes
2. **Round-Robin**: Distribuição equitativa circular
3. **Embaralhamento**: Aleatoriedade para justiça
4. **Persistência**: Atribuições mantidas enquanto vendedor online

#### Ciclo de Status
```
disponivel → atribuido → contatado
     ↑           ↓
     └───────────┘
    (se vendedor sair)
```

### Períodos de Clientes

| Período | Dias Inativos | Prioridade | Badge |
|---------|---------------|------------|-------|
| Urgente | 30-45 | Máxima | 🔥 |
| Atenção | 45-60 | Alta | ⚠️ |
| Moderado | 60-90 | Média | ⏰ |
| Crítico | >90 | Baixa | 📊 |

---

## 🔐 API Endpoints

### Autenticação (`/api/auth`)
- `POST /login` - Login vendedor/admin
- `POST /logout/{vendedor_id}` - Logout
- `GET /vendedores` - Lista vendedores

### Vendedor (`/api/vendedor`)
- `GET /meus-clientes/{vendedor_id}` - Clientes atribuídos
- `POST /marcar-contatado/{vendedor_id}` - Marcar contato
- `GET /estatisticas/{vendedor_id}` - Estatísticas pessoais

### Admin (`/api/admin`)
- `GET /clientes-por-periodo` - Clientes organizados
- `GET /todos-clientes` - Lista completa
- `POST /realocar-cliente` - Realocação manual
- `POST /redistribuir-todos` - Redistribuição completa
- `POST /liberar-cliente/{cliente_id}` - Liberar cliente
- `GET /estatisticas-gerais` - Estatísticas do sistema

---

## 🐛 Bugs Corrigidos

### 1. ❌ Clientes Pendentes = 0
**Problema**: Após distribuição, status mudava para "atribuido" e não era mais encontrado na próxima redistribuição.

**Solução**: 
- Busca agora por `status != "contatado"` ao invés de `status == "pendente"`
- Gestão correta de estados disponível/atribuído/contatado

### 2. ❌ Redistribuição Quebrada
**Problema**: Clientes não eram redistribuídos corretamente ao entrar/sair vendedores.

**Solução**:
- Lógica completamente reescrita
- Separação entre clientes com/sem atribuição
- Limpeza de atribuições de vendedores offline

### 3. ❌ Contadores Incorretos
**Problema**: Estatísticas não refletiam realidade.

**Solução**:
- Queries otimizadas
- Contagem baseada em ClienteVendedor ao invés de Cliente.status

---

## 💡 Dicas de Uso

### Para Vendedores
1. Faça login no início do turno
2. Priorize clientes com badge 🔥 Urgente
3. Adicione observações ao marcar contato
4. Use a busca para localizar clientes rapidamente
5. Faça logout ao sair para liberar clientes

### Para Administradores
1. Monitore a aba "Clientes por Período" para visão rápida
2. Use "Performance Vendedores" para avaliar equipe
3. Realoque manualmente clientes específicos quando necessário
4. Use "Redistribuir Todos" apenas quando necessário (ex: início do dia)
5. Libere clientes travados para torná-los disponíveis

---

## 🧪 Testando o Sistema

### Cenário 1: Múltiplos Vendedores
1. Abra 3 abas do navegador
2. Faça login com 3 vendedores diferentes
3. Observe a distribuição automática
4. Faça logout em uma aba
5. Veja os clientes sendo redistribuídos

### Cenário 2: Admin Gerenciando
1. Faça login como Admin
2. Vá para "Todos os Clientes"
3. Realoque um cliente para vendedor específico
4. Abra aba do vendedor e veja cliente aparecer
5. Teste "Redistribuir Todos"

### Cenário 3: Marcação de Contato
1. Login como vendedor
2. Escolha um cliente
3. Marque como contatado com observações
4. Vá no painel admin
5. Veja cliente marcado como contatado

---

## 📊 Dados de Teste

### Clientes Gerados
- **30 clientes**: 30-45 dias (Urgente)
- **25 clientes**: 45-60 dias (Atenção)
- **20 clientes**: 60-90 dias (Moderado)
- **15 clientes**: >90 dias (Crítico)
- **20 clientes**: <30 dias (Ativos - não aparecem)

### Total: 110 clientes no banco

---

## 🚀 Melhorias Futuras

### Curto Prazo
- [ ] Histórico de contatos
- [ ] Filtros avançados
- [ ] Exportar relatórios (CSV/PDF)
- [ ] Notificações push

### Médio Prazo
- [ ] Integração WhatsApp
- [ ] Templates de mensagens
- [ ] Agendamento de contatos
- [ ] Metas por vendedor

### Longo Prazo
- [ ] Dashboard com gráficos
- [ ] Machine Learning para priorização
- [ ] App mobile
- [ ] Integração CRM externo

---

## 🔒 Segurança

⚠️ **Importante**: Este é um sistema de demonstração.

Para produção, implemente:
- ✅ Hash de senhas (bcrypt)
- ✅ JWT para autenticação
- ✅ HTTPS
- ✅ Rate limiting
- ✅ Validação de entrada robusta
- ✅ Logs de auditoria

---

## 🆘 Solução de Problemas

### Erro: "table vendedores has no column named is_admin"
```bash
rm crm_kanban.db
python app.py
```

### Clientes não aparecem
1. Verifique se há vendedores online
2. Use "Redistribuir Todos" no painel admin
3. Verifique logs do servidor

### WebSocket desconecta
- Normal após inatividade
- Reconecta automaticamente
- Se persistir, recarregue a página

---

## 📝 Changelog

### v2.0.0 (2026-01-10)
- ✅ Correção crítica do sistema de distribuição
- ✅ Adição do painel administrativo completo
- ✅ Reorganização da arquitetura do projeto
- ✅ Melhorias na interface (badges, períodos)
- ✅ API modular e escalável
- ✅ Documentação completa atualizada

### v1.0.0 (2026-01-10)
- ✨ Lançamento inicial
- ✅ Sistema básico de CRM
- ✅ Distribuição automática
- ✅ Interface vendedor

---

**Desenvolvido com ❤️ usando FastAPI, SQLAlchemy e tecnologias modernas**

**Sistema pronto para uso com arquitetura profissional** 🚀
