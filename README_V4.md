# 🎯 CRM Kanban v4.0 - Sistema Exclusivo Administrador

![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-teal.svg)

## 🚀 MUDANÇA RADICAL - v4.0

Sistema completamente reformulado para ser **EXCLUSIVO DO ADMINISTRADOR** com funcionalidades avançadas de customização!

### ✨ O que mudou:

#### ❌ **Removido:**
- Sistema de login para vendedores
- Perfis de vendedores individuais
- Autenticação de vendedores

#### ✅ **Novo Conceito:**
- **Vendedores são apenas IDs numéricos** (#1, #2, #3...)
- **Administrador tem controle total** sobre distribuição
- **Customização avançada** com atributos configuráveis
- **Exportação inteligente** para compartilhar com vendedores externos

---

## 🎯 Funcionalidades Principais

### 1. 🔢 **Sistema de Vendedores Numéricos**
- Configure de **1 a 50 vendedores**
- Vendedores são apenas identificadores (#1, #2, #3...)
- Sem login, sem senhas, sem complicação

### 2. ⚙️ **Distribuição Customizável por Atributos**

Escolha o critério de distribuição:
- **⏱️ Dias sem Comprar** - Urgência (clientes mais antigos primeiro)
- **⭐ Prioridade** - 0-10 (maior prioridade primeiro)
- **📊 Complexidade** - 1-10 (casos mais complexos primeiro)
- **💰 Potencial de Venda** - Valor estimado (maiores valores primeiro)
- **💵 Valor Total Compras** - Histórico (melhores clientes primeiro)
- **🎲 Aleatório** - Distribuição randômica

### 3. 🎚️ **Pesos Personalizados por Vendedor**

Configure quanto cada vendedor recebe:
- **1.0** = Normal (distribuição padrão)
- **1.5** = 50% a mais que o normal
- **2.0** = 100% a mais (dobro)
- **0.5** = 50% menos que o normal
- **0.3** = 30% do normal

**Exemplo prático:**
- 3 vendedores com pesos [1.0, 1.5, 0.5]
- 100 clientes disponíveis
- Resultado: Vendedor #1 = 33, Vendedor #2 = 50, Vendedor #3 = 17

### 4. 📋 **Exportação Avançada**

**Por vendedor individual:**
- Clique no card do vendedor
- Copie a lista formatada
- Envie por WhatsApp, Email, etc.

**Todos os vendedores de uma vez:**
- Botão "Copiar Todos Vendedores"
- Recebe lista completa organizada
- Ideal para relatórios ou distribuição em massa

### 5. 🎨 **Atributos Customizáveis por Cliente**

Cada cliente tem:
- **⭐ Prioridade** (0-10) - Defina importância
- **📊 Complexidade** (1-10) - Nível de dificuldade
- **💰 Potencial de Venda** - Estimativa de valor futuro
- **📝 Observações** - Notas personalizadas

### 6. 📊 **Dashboard Avançado**

- Estatísticas gerais do sistema
- Cards individuais por vendedor
- Taxa de conversão
- Potencial total de vendas
- Tabela completa com filtros e ordenação

---

## 🚀 Como Usar

### Instalação

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o sistema
python app_admin_only.py

# 3. Acessar no navegador
http://localhost:8000
```

### Login Padrão
- **Usuário:** `admin`
- **Senha:** `admin123`

---

## 📖 Guia de Uso

### 1️⃣ **Configurar Vendedores**

1. Acesse o painel de distribuição
2. Defina **Número de Vendedores** (ex: 5)
3. Configure os **Pesos** de cada um:
   - Vendedor #1: 1.0 (normal)
   - Vendedor #2: 1.5 (recebe 50% a mais - vendedor sênior)
   - Vendedor #3: 1.0 (normal)
   - Vendedor #4: 0.8 (recebe 20% a menos - vendedor júnior)
   - Vendedor #5: 1.2 (recebe 20% a mais)

### 2️⃣ **Escolher Critério de Distribuição**

Selecione o atributo que define a ordem:
- **Urgência** → Use "Dias sem Comprar"
- **Importância** → Use "Prioridade"
- **Dificuldade** → Use "Complexidade"
- **Valor** → Use "Potencial de Venda" ou "Valor Total"

### 3️⃣ **Distribuir Clientes**

1. Clique em **"Distribuir Clientes"**
2. Sistema aloca automaticamente baseado:
   - Critério escolhido
   - Pesos configurados
   - Clientes disponíveis
3. Veja resultado detalhado por vendedor

### 4️⃣ **Exportar e Compartilhar**

**Opção 1 - Vendedor individual:**
```
1. Clique no card do vendedor
2. Veja lista formatada
3. Clique "Copiar"
4. Cole no WhatsApp/Email
```

**Opção 2 - Todos de uma vez:**
```
1. Clique "Copiar Todos Vendedores"
2. Recebe arquivo completo
3. Distribua como preferir
```

### 5️⃣ **Gerenciar Atributos**

Para cada cliente você pode:
- ✏️ **Editar** - Ajustar prioridade, complexidade e potencial
- ✅ **Marcar Contatado** - Registrar que foi abordado
- 📝 **Adicionar Observações** - Notas importantes

### 6️⃣ **Redistribuir**

Precisa realocar clientes?
1. Clique **"Liberar Todos"**
2. Ajuste configurações
3. Clique **"Distribuir Clientes"** novamente

---

## 🎨 Exemplo de Uso Real

### Cenário: Empresa com 4 vendedores

**Configuração:**
- **4 vendedores**
- **Vendedor #1** (Sênior): Peso 1.5
- **Vendedor #2** (Pleno): Peso 1.0
- **Vendedor #3** (Júnior): Peso 0.7
- **Vendedor #4** (Pleno): Peso 1.0

**Critério:** Potencial de Venda (maiores valores primeiro)

**Resultado:**
- Vendedor #1 recebe 35% dos clientes (os de maior potencial)
- Vendedor #2 recebe 24% dos clientes
- Vendedor #3 recebe 17% dos clientes (menor carga)
- Vendedor #4 recebe 24% dos clientes

**Exportação:**
Admin copia lista de cada vendedor e envia por WhatsApp:

```
═══════════════════════════════════════════════
    CLIENTES PARA: VENDEDOR #1
    Data: 12/01/2026 às 14:30:15
═══════════════════════════════════════════════

#001 - JOÃO SILVA 🔥 URGENTE
─────────────────────────────────────────────
📱 Celular:      (11) 99876-5432
📧 Email:        joao.silva@email.com
⏱️  Sem comprar:  35 dias
💰 Total gasto:  R$ 15.430,00
🎯 Potencial:    R$ 25.000,00
⭐ Prioridade:   9/10
📊 Complexidade: 7/10
🗓️  Última compra: 08/12/2025

[... mais clientes ...]
```

---

## 🔥 Vantagens do Novo Sistema

### Para o Administrador:
✅ **Controle Total** - Você decide tudo  
✅ **Flexibilidade Máxima** - Configure como quiser  
✅ **Sem Complicação** - Sem gerenciar logins de vendedores  
✅ **Customização Infinita** - Pesos, atributos, critérios  
✅ **Exportação Fácil** - Copiar e colar instantâneo  

### Para a Empresa:
✅ **Eficiência** - Distribuição inteligente  
✅ **Transparência** - Tudo registrado e rastreável  
✅ **Escalabilidade** - De 1 a 50 vendedores  
✅ **Adaptabilidade** - Mude critérios quando quiser  

---

## 📊 Estrutura de Dados

### Cliente
```python
{
    "id": 1,
    "nome": "João Silva",
    "celular": "(11) 99876-5432",
    "email": "joao@email.com",
    "data_ultima_compra": "2025-12-08",
    "valor_total_compras": 15430.00,
    "dias_sem_comprar": 35,
    "vendedor_id": 1,  # ID numérico
    "prioridade": 9,   # 0-10
    "complexidade": 7,  # 1-10
    "potencial_venda": 25000.00,
    "contatado": false,
    "observacoes": "Cliente VIP"
}
```

---

## 🛠️ Tecnologias

- **Backend:** Python + FastAPI
- **Banco:** SQLite (pode migrar para PostgreSQL)
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Fake Data:** Faker (dados brasileiros)

---

## 📝 Notas Importantes

1. **Vendedores não têm acesso ao sistema** - São apenas IDs
2. **Admin é responsável por distribuir as listas** - Via WhatsApp, Email, etc.
3. **Pesos são flexíveis** - Ajuste conforme capacidade de cada vendedor
4. **Redistribuição é livre** - Libere e distribua quantas vezes quiser
5. **Dados são persistentes** - Tudo fica salvo no banco

---

## 🎯 Casos de Uso

### 1. Empresa com Vendedores Externos
- Admin distribui via WhatsApp
- Vendedores trabalham por conta própria
- Admin marca contatados manualmente

### 2. Equipe com Diferentes Níveis
- Sênior recebe mais clientes complexos (peso 1.5)
- Júnior recebe menos clientes (peso 0.5)
- Distribuição por complexidade

### 3. Campanhas Específicas
- Alta prioridade = clientes VIP
- Distribuir por potencial de venda
- Focar nos melhores leads

### 4. Balanceamento de Carga
- Vendedor sobrecarregado = peso 0.5
- Vendedor com capacidade = peso 1.5
- Redistribuir semanalmente

---

## 🚀 Próximos Passos

Sugestões de melhorias:
- [ ] Exportação para Excel/CSV
- [ ] Integração com WhatsApp API
- [ ] Histórico de distribuições
- [ ] Relatórios de performance
- [ ] Agendamento automático de redistribuição
- [ ] Multi-tenancy (várias empresas)

---

## 📞 Suporte

Sistema desenvolvido para máxima customização e controle administrativo.

**Login padrão:**
- Usuário: `admin`
- Senha: `admin123`

---

**Versão:** 4.0.0  
**Data:** Janeiro 2026  
**Status:** ✅ Produção
