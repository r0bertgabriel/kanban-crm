# 🎯 CRM Kanban v3.0 - Sistema Administrativo Simplificado

![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-teal.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

## 🔥 O QUE MUDOU NA V3.0

❌ **REMOVIDO**: Telas de vendedores, WebSocket complexo, sistema de login/logout de vendedores  
✅ **SIMPLIFICADO**: Apenas painel admin com funcionalidade de exportação para copiar e colar  
✅ **CORRIGIDO**: Todos os bugs de distribuição e atribuição  
✅ **FOCADO**: Sistema limpo para gestão centralizada de clientes  

## 📋 Descrição

Sistema **SIMPLIFICADO** de CRM focado em **gestão administrativa** de clientes inativos. O administrador visualiza todos os clientes, atribui para vendedores e **exporta listas via texto** para enviar por WhatsApp/Telegram.

### ✨ Funcionalidades

#### Painel Administrativo Único
- 📊 **Visualização completa** de todos os clientes
- 🔍 **Filtros avançados** por período, status, vendedor
- 📤 **Atribuição em lote** de clientes a vendedores
- 📋 **Exportação de texto** formatado para copiar e colar
- ✅ **Marcação de contatos** realizados
- 🔓 **Liberação** de clientes para reatribuição
- 📈 **Estatísticas gerais** do sistema

#### Períodos de Inatividade
| Período | Dias | Badge |
|---------|------|-------|
| Urgente | 30-45d | 🔥 |
| Atenção | 45-60d | ⚠️ |
| Moderado | 60-90d | ⏰ |
| Crítico | >90d | 📊 |
| Ativo | <30d | ✅ |

## 🚀 Instalação e Uso

### 1. Instalar Dependências

```bash
pip install fastapi uvicorn sqlalchemy faker pydantic
```

### 2. Iniciar Servidor

```bash
python3 app_v3.py
```

### 3. Acessar Sistema

```
http://localhost:8000
```

**Login:**
- Usuário: `admin`
- Senha: `admin123`

## 📁 Estrutura do Projeto

```
kanban-crm/
├── app_v3.py                  # ⭐ Aplicação única (350 linhas)
├── static/
│   └── admin_v3.html          # Interface admin completa
├── crm_kanban.db              # Banco SQLite (auto-criado)
└── README_V3.md               # Este arquivo
```

## 🎮 Como Usar

### 1. Login
- Acesse http://localhost:8000
- Usuário: `admin`, Senha: `admin123`
- Clique em "Entrar"

### 2. Visualizar Clientes
- **110 clientes** carregados automaticamente
- **5 vendedores** disponíveis
- Filtros por período, status, vendedor
- Busca por nome, telefone ou email

### 3. Atribuir Clientes a Vendedor

**Método 1: Seleção Manual**
1. Marque checkboxes dos clientes desejados
2. Clique em "📤 Atribuir Selecionados"
3. Digite o nome do vendedor
4. Confirme

**Método 2: Seleção por Filtro**
1. Use filtros para isolar clientes (ex: Urgente + Disponível)
2. Clique em "✅ Selecionar Todos"
3. Atribua ao vendedor

### 4. Exportar para Vendedor

**Botão "Exportar [Vendedor]"** (parte inferior)
1. Clique no botão do vendedor desejado
2. Modal abre com texto formatado
3. Clique em "📋 Copiar"
4. Cole no WhatsApp/Telegram/Email do vendedor

**Formato da Exportação:**
```
═══════════════════════════════════════════════
    CLIENTES PARA: JOÃO SILVA
    Data: 10/01/2026 21:50
═══════════════════════════════════════════════

1. Maria da Silva
   📱 (11) 91234-5678
   📧 maria@email.com
   📊 Sem comprar há 35 dias
   💰 Total compras: R$ 5.432,00
   🗓️  Última compra: 06/12/2025
   ─────────────────────────────────────────

2. José Santos
   ...

Total: 12 cliente(s)
```

### 5. Gerenciar Clientes

**Liberar Cliente** (remove atribuição)
- Clique no botão "🔓 Liberar" na linha do cliente
- Cliente volta para status "Disponível"

**Marcar como Contatado**
- Clique no botão "✅ Contatado"
- Digite observações (opcional)
- Cliente é marcado como contatado

**Atualizar Dados**
- Clique no botão "🔄 Atualizar" no topo
- Recarrega clientes e estatísticas

## 📊 Dados Populados Automaticamente

### Clientes (110 total)
- 30 clientes **Urgentes** (30-45 dias)
- 25 clientes **Atenção** (45-60 dias)
- 20 clientes **Moderados** (60-90 dias)
- 15 clientes **Críticos** (>90 dias)
- 20 clientes **Ativos** (<30 dias)

### Vendedores (5 total)
- João Silva
- Maria Santos
- Pedro Oliveira
- Ana Costa
- Carlos Ferreira

### Dados Fictícios Brasileiros
- Nomes gerados com Faker (pt_BR)
- Celulares com DDDs reais (11, 21, 31, etc)
- Emails válidos
- Valores de compra realistas (R$ 500 - R$ 15.000)

## 🌐 API Endpoints

### Autenticação
- `POST /api/login` - Login administrativo

### Clientes
- `GET /api/clientes` - Lista todos com informações de período
- `POST /api/atribuir` - Atribui clientes a vendedor
- `POST /api/liberar/{id}` - Libera cliente
- `POST /api/marcar-contatado/{id}` - Marca como contatado

### Vendedores
- `GET /api/vendedores` - Lista todos os vendedores

### Exportação
- `GET /api/exportar/{vendedor}` - Exporta texto formatado

### Estatísticas
- `GET /api/estatisticas` - Estatísticas gerais do sistema

## 🐛 Correções da V3.0

### Problemas Resolvidos
✅ **Sistema complexo demais** → Simplificado para apenas admin  
✅ **Bugs de distribuição automática** → Removido, agora é manual  
✅ **WebSocket falhando** → Removido completamente  
✅ **Vendedores online/offline** → Conceito eliminado  
✅ **Arquivos duplicados** (main.py) → Removidos  
✅ **Erros de tipo SQLAlchemy** → Modelos simplificados  
✅ **Imports não usados** → Código limpo  

### Arquitetura
- **V1/V2**: 11 arquivos Python, 2 interfaces, WebSocket, rotas complexas
- **V3**: 2 arquivos (app_v3.py + admin_v3.html) - TUDO CENTRALIZADO

## 💡 Fluxo de Trabalho Recomendado

### Início do Dia
1. Admin acessa sistema
2. Filtra clientes urgentes disponíveis
3. Atribui 15-20 clientes para cada vendedor
4. Exporta lista de cada vendedor
5. Envia via WhatsApp/Telegram

### Durante o Dia
- Admin marca clientes contatados conforme feedback dos vendedores
- Realoca clientes se necessário
- Libera clientes que não foram contactados

### Fim do Dia
- Admin visualiza estatísticas
- Verifica taxa de conversão por vendedor
- Planeja redistribuição para próximo dia

## 🔒 Notas de Segurança

⚠️ **Sistema de demonstração** - Para produção:
- Adicionar hash de senhas (bcrypt)
- Implementar tokens JWT
- Habilitar HTTPS
- Adicionar rate limiting
- Validar inputs rigorosamente

## 📈 Estatísticas Exibidas

- **Total de Clientes**: Quantidade no sistema
- **Disponíveis**: Sem vendedor atribuído
- **Atribuídos**: Com vendedor, aguardando contato
- **Contatados**: Já processados

**Por Vendedor:**
- Total de clientes
- Pendentes (não contatados)
- Contatados
- Taxa de conversão (%)

## 🎯 Vantagens da V3.0

✅ **Simplicidade**: 1 arquivo Python, 1 HTML  
✅ **Estabilidade**: Sem bugs de distribuição automática  
✅ **Controle**: Admin tem controle total manual  
✅ **Exportação**: Fácil envio para vendedores  
✅ **Manutenção**: Código limpo e fácil de modificar  
✅ **Performance**: Sem WebSocket, sem overhead  

## 🚀 Próximas Melhorias (Opcional)

- [ ] Histórico de atribuições
- [ ] Gráficos de conversão por período
- [ ] Exportação em Excel/CSV
- [ ] Templates de mensagem personalizados
- [ ] Agendamento de follow-ups
- [ ] Integração direta com WhatsApp API
- [ ] Backup automático do banco

## 📞 Comandos Úteis

### Resetar Banco de Dados
```bash
rm crm_kanban.db
python3 app_v3.py
```

### Verificar Porta em Uso
```bash
lsof -ti:8000
```

### Matar Servidor
```bash
pkill -f "python.*app"
```

### Rodar em Produção
```bash
uvicorn app_v3:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📄 Licença

Sistema desenvolvido para uso interno. Código livre para modificações.

---

## ⚡ Quick Start

```bash
# 1. Instalar
pip install fastapi uvicorn sqlalchemy faker pydantic

# 2. Executar
python3 app_v3.py

# 3. Acessar
# http://localhost:8000
# Login: admin / admin123
```

**🎉 Sistema operacional e pronto para uso!**
