# 🎯 CRM Kanban v2.0 - Sistema de Gestão de Vendas

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

Sistema completo de CRM com distribuição automática e inteligente de clientes entre vendedores, desenvolvido em Python com FastAPI e interface web moderna.

## ✨ Novidades da v2.0

- 🐛 **Bug Crítico Corrigido**: Sistema de distribuição totalmente reescrito e funcional
- 👑 **Painel Administrativo**: Interface completa para gestão de clientes e vendedores
- 📁 **Arquitetura Modular**: Código organizado e escalável
- 🎨 **Interface Aprimorada**: Badges de urgência e organização por períodos
- 📊 **Performance**: Dashboard com métricas em tempo real

## 📋 Descrição

Este sistema foi projetado para otimizar o trabalho de equipes de vendas, identificando automaticamente clientes que não realizaram compras entre 30 e 60 dias e distribuindo-os de forma equitativa entre os vendedores online.

### ✨ Funcionalidades Principais

#### Para Vendedores
- **🔍 Identificação Automática**: Detecta clientes inativos (30-60 dias sem comprar)
- **🔄 Distribuição Inteligente**: Realoca clientes automaticamente quando vendedores entram/saem online
- **📊 Dashboard em Tempo Real**: Estatísticas e atualizações instantâneas via WebSocket
- **🔥 Badges de Urgência**: Priorização visual (30-45 dias = Urgente, 45-60 = Atenção)
- **✅ Controle de Contatos**: Marcação de clientes contatados com observações
- **🔍 Busca Rápida**: Localização instantânea por nome, telefone ou email

#### Para Administradores
- **📅 Visão por Períodos**: Clientes organizados em 4 categorias (30-45d, 45-60d, 60-90d, >90d)
- **🔄 Realocação Manual**: Atribuir clientes a vendedores específicos
- **📊 Estatísticas Gerais**: Métricas completas do sistema
- **👥 Performance**: Taxa de conversão por vendedor
- **🔓 Gestão Flexível**: Liberar e redistribuir clientes
- **📋 Tabela Completa**: Visualização de todos os clientes com filtros

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou navegue até o diretório do projeto**

```bash
cd kanban-crm
```

2. **Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### Iniciar o Servidor

```bash
python app.py

# OU
./start.sh
```

O servidor iniciará em: `http://localhost:8000`

### Acessar o Sistema

#### Vendedores
1. Acesse: `http://localhost:8000`
2. Faça login com um dos vendedores disponíveis
3. Senha: `123456`

**Vendedores Disponíveis:**
- João Silva
- Maria Santos
- Pedro Oliveira
- Ana Costa
- Carlos Ferreira

#### Administrador
1. Acesse: `http://localhost:8000`
2. Selecione "Admin (Administrador)"
3. Senha: `admin123`
4. Será redirecionado automaticamente para `/admin`

### Fluxo de Trabalho

1. **Login**: Escolha seu nome e faça login
2. *app.py                      # Aplicação principal FastAPI
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
├── static/                     # Frontend
│   ├── index.html              # Interface vendedor
│   ├── script.js               # Lógica vendedor
│   ├── admin.html              # Interface admin
│   ├── admin-script.js         # Lógica admin
│   ├── styles.css              # Estilos comuns
│   └── admin-styles.css        # Estilos admin
├── requirements.txt            # Dependências
├── README.md                   # Este arquivo
├── DOCUMENTACAO_V2.md          # Documentação completa
├── ARQUITETURA.md              # Arquitetura do sistema
└── V1_VS_V2.md                 # Comparação de versões
kanban-crm/
├── main.py                 # Backend FastAPI + Lógica de negócio
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── crm_kanban.db          # Banco de dados SQLite (gerado automaticamente)
└── static/                # Frontend
    ├── index.html         # Interface HTML
    ├── styles.css         # Estilos CSS
    └── script.js          # Lógica JavaScript
```

## 🔧 Características Técnicas

### Backend

- **Framework**: FastAPI (Python)
- **Banco de Dados**: SQLite com SQLAlchemy ORM
- **WebSocket**: Atualizações em tempo real
- **Autenticação**: Sistema básico de login
- **API RESTful**: Endpoints documentados automaticamente

### Frontend

- **HTML5/CSS3**: Interface moderna e responsiva
- **JavaScript Vanilla**: Sem frameworks externos
- **WebSocket Client**: Comunicação bidirecional
- Não foram marcados como contatados

### Períodos de Prioridade

| Período | Dias Inativos | Prioridade | Badge |
|---------|---------------|------------|-------|
| Urgente | 30-45 | Máxima | 🔥 |
| Atenção | 45-60 | Alta | ⚠️ |
| Moderado | 60-90 | Média | ⏰ |
| Crítico | >90 | Baixa | 📊 |

### Distribuição de Clientes

- Clientes são distribuídos automaticamente entre vendedores **online**
- Distribuição é feita de forma equitativa (round-robin com embaralhamento)
- Quando um vendedor sai, seus clientes não contatados são redistribuídos
- Quando um vendedor entra, recebe sua parte dos clientes disponíveis
- Admin pode realocar manualmente clientes para vendedores específico
- `pedidos`: Histórico de pedidos
- `cliente_vendedor`: Atribuição de clientes aos vendedores

## 📊 Regras de Negócio

### Identificação de Clientes

O sistema identifica clientes que:
- Não compraram nos últimos 30 a 60 dias
- Possuem histórico de compras anterior
- Estão com status "pendente"

##1 administrador
- 5 vendedores
- 10 produtos variados
- **30 clientes urgentes (30-45 dias)** - Prioridade máxima
- **25 clientes atenção (45-60 dias)** - Prioridade alta
- 20 clientes moderados (60-90 dias)
- 15 clientes críticos (>90 dias)
- 20 clientes ativos (compraram recentemente)
- Números de celular brasileiros fictícios com DDDs reais
 (`/api/auth`)
- `POST /login` - Login de vendedor ou administrador
- `POST /logout/{vendedor_id}` - Logout
- `GET /vendedores` - Lista todos os vendedores

### Vendedor (`/api/vendedor`)
- `GET /meus-clientes/{vendedor_id}` - Clientes do vendedor
- `POST /marcar-contatado/{vendedor_id}` - Marcar cliente como contatado
- `GET /estatisticas/{vendedor_id}` - Estatísticas do vendedor

### Admin (`/api/admin`)
- `GET /clientes-por-periodo` - Clientes organizados por período
- `GET /todos-clientes` - Lista completa de clientes
- `POST /realocar-cliente` - Realocação manual
- `POST /redistribuir-todos` - Redistribuição completa
- `POST /liberar-cliente/{cliente_id}` - Liberar cliente
- `GET /estatisticas-gerais` - Estatísticas do sistema

### WebSocket
- `WS /ws/{user_id}` - Conexão para atualizações em tempo real

**📖 Documentação interativa:** http://localhost:8000/docs
- `POST /api/login` - Login de vendedor
- `POST /api/logout/{vendedor_id}` - Logout

### Vendedores
- `GET /api/vendedores` - Lista todos os vendedores

### Clientes
- `GET /api/meus-clientes/{vendedor_id}` - Clientes do vendedor
- `POST /api/marcar-contatado/{vendedor_id}` - Marcar cliente como contatado

### Estatísticas
- `GET /api/estatisticas/{vendedor_id}` - Estatísticas do vendedor

### WebSocket
- `WS /ws/{vendedor_id}` - Conexão para atualizações em tempo real

## 🎨 Interface

### Tela de Login
- Seleção de vendedor via dropdown
- Campo de senha
- Validação de credenciais

### Dashboard
- Cabeçalho com informações do usuário
- Contador de vendedores online
- Cards de estatísticas:
  - Clientes Pendentes
  - Clientes Contatados
  - Total Atribuídos
- Lista de vendedores online
- Grid de clientes para contatar
- Busca em tempo real
- Modal para marcar contato

## 🔒 Segurança

**Nota**: Este é um sistema de demonstração. Para ambiente de produção, implemente:
- Hash de senhas (bcrypt)
- Tokens JWT para autenticação
- HTTPS
- Validação de entrada robusta
- Rate limiting
- CORS configurado adequadamente

## 📝 Dados de Exemplo

### Números de Celular
Formato: `+55 (XX) 9XXXX-XXXX`
DDDs rea: "table vendedores has no column named is_admin"

```bash
# Deletar banco antigo e reiniciar
rm crm_kanban.db
python app.py
```

### Porta 8000 já está em uso

```bash
# Matar processo na porta
pkill -f "python app.py"

# OU usar outra porta
uvicorn app:app --host 0.0.0.0 --port 8001
```

### Banco de dados corrompido

```bash
# Delete o arquivo e reinicie (dados serão recriados)
rm crm_kanban.db
python app.py
```

### Clientes não aparecem

1. Verifique se há vendedores online
### Curto Prazo
- [ ] Testes automatizados (pytest)
- [ ] Histórico completo de contatos
- [ ] Filtros avançados e ordenação
- [ ] Exportar relatórios (CSV/Excel/PDF)

### Médio Prazo
- [ ] Integração WhatsApp/Telegram
- [ ] Templates de mensagens personalizadas
- [ ] Agendamento de contatos
- [ ] Sistema de metas e gamificação
- [ ] Notificações push em tempo real

### Longo Prazo
- [ ] Dashboard com gráficos interativos
- [ ] Machine Learning para priorização
- [ ] App mobile (React Native)
- [ ] Integração com CRMs externos
- [ ] Multi-tenancy (múltiplas empresas)

## 🔒 Notas de Seguraa porta
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Banco de dados corrompido

```bash
# Delete o arquivo e reinicie (dados serão recriados)
rm crm_kanban.db
python main.py
```

## 🚀 Próximas Melhorias

- [ ] Sistema de notificações push
- [ ] Histórico de contatos
- [ ] Relatórios e exportação de dados
- [ ] Integração com WhatsApp/Telegram
- [ ] Sistema de metas por vendedor
- [ ] Dashboard do gestor (visão geral)
- [ ] Logs de auditoria
- [ ] Backup automático do banco

## 📄 Licença

Este projeto é de código aberto para fins educacionais e de demonstração.

## 👨‍💻 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação acima
2. Confira os logs do servidor
3. Revise o código fonte comentado

---

**Desenvolvido com ❤️ usando FastAPI e tecnologias modernas**
