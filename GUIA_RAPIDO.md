# 🎯 Guia Rápido - CRM Kanban

## ⚡ Início Rápido

### 1. Instalar e Iniciar

```bash
# Opção 1: Usar o script de inicialização
./start.sh

# Opção 2: Manualmente
pip install -r requirements.txt
python main.py
```

### 2. Acessar o Sistema

Abra seu navegador em: **http://localhost:8000**

### 3. Fazer Login

Escolha um vendedor e use a senha: **123456**

**Vendedores disponíveis:**
- João Silva
- Maria Santos  
- Pedro Oliveira
- Ana Costa
- Carlos Ferreira

---

## 💡 Como o Sistema Funciona

### Fluxo de Trabalho

1. **Login** → O vendedor entra no sistema
2. **Distribuição Automática** → Clientes são atribuídos automaticamente
3. **Visualização** → Vendedor vê seus clientes na tela
4. **Contato** → Vendedor liga/envia mensagem para o cliente
5. **Confirmação** → Marca o cliente como contatado
6. **Redistribuição** → Sistema realoca clientes de vendedores offline

### Critérios de Seleção de Clientes

O sistema identifica automaticamente clientes que:
- ✅ Não compraram nos **últimos 30 a 60 dias**
- ✅ Possuem histórico de compras anterior
- ✅ Estão disponíveis para contato

### Distribuição Inteligente

- 🔄 **Automática**: Clientes são distribuídos ao fazer login
- ⚖️ **Equitativa**: Divisão justa entre vendedores online
- 🔁 **Dinâmica**: Redistribui quando vendedores entram/saem
- 🎯 **Eficiente**: Evita duplicação de contatos

---

## 🎨 Funcionalidades da Interface

### Dashboard

**Estatísticas em Tempo Real:**
- 📊 Clientes Pendentes
- ✅ Clientes Contatados
- 📱 Total Atribuídos

**Lista de Vendedores:**
- 🟢 Verde = Online
- ⚪ Cinza = Offline

**Grid de Clientes:**
- 👤 Nome do cliente
- 📱 Celular formatado (XX) 9XXXX-XXXX
- 📧 Email
- 🕒 Tempo desde última compra
- 💰 Valor total de compras

### Ações Disponíveis

1. **🔍 Buscar**: Digite nome, telefone ou email
2. **🔄 Atualizar**: Recarrega os dados
3. **✅ Marcar Contatado**: Registra o contato feito
4. **📝 Observações**: Adiciona notas sobre o contato

---

## 📊 Dados do Sistema

### Banco de Dados Populado

O sistema popula automaticamente com:

- **5 Vendedores** prontos para usar
- **50 Clientes** inativos (30-60 dias) → **Alvos principais**
- **20 Clientes** ativos (compraram recentemente)
- **30 Clientes** muito inativos (>60 dias)
- **10 Produtos** variados
- **Histórico** de pedidos para cada cliente

### Números de Celular

Todos os números são **fictícios** mas seguem o padrão brasileiro:
- Formato: `+55 (XX) 9XXXX-XXXX`
- DDDs reais: 11, 21, 31, 41, 51, 61, 71, 81, 85, 91
- Prefixo 9 (celular)

---

## 🔧 Funcionalidades Técnicas

### Atualizações em Tempo Real

- ⚡ **WebSocket** conecta cada vendedor
- 🔔 Notificações instantâneas de mudanças
- 🔄 Auto-refresh a cada 30 segundos

### Persistência de Dados

- 💾 **SQLite** armazena todos os dados
- 🗄️ Arquivo: `crm_kanban.db`
- 🔄 Repopula a cada reinicialização

### API REST

- 📡 Endpoints documentados automaticamente
- 📚 Docs em: `http://localhost:8000/docs`
- 🔍 Explorar API: `http://localhost:8000/redoc`

---

## 🎯 Casos de Uso

### Cenário 1: Início do Dia

1. **8h00** - João entra online
   - Recebe 50 clientes para contatar

2. **8h15** - Maria entra online
   - Sistema redistribui: 25 para João, 25 para Maria

3. **8h30** - Pedro entra online
   - Nova redistribuição: ~17 para cada um

### Cenário 2: Durante o Dia

1. João marca 5 clientes como contatados
   - Não voltam para redistribuição
   - João mantém os clientes restantes

2. Pedro sai para almoço (logout)
   - Clientes não contatados de Pedro são redistribuídos
   - João e Maria recebem esses clientes

### Cenário 3: Novos Clientes

Quando o banco é repopulado (reiniciar servidor):
- ✅ Novos clientes inativos são gerados
- ✅ Datas são atualizadas
- ✅ Histórico de contatos é mantido

---

## 🚨 Dicas Importantes

### Para Vendedores

- ✅ **Faça login** ao começar o dia
- 📱 **Ligue ou envie WhatsApp** para os clientes
- ✅ **Marque como contatado** após o contato
- 📝 **Adicione observações** importantes
- 🔄 **Clique em atualizar** periodicamente
- 🚪 **Faça logout** ao sair

### Para Gestores

- 👥 Monitore vendedores online
- 📊 Acompanhe estatísticas em tempo real
- 🔍 Use busca para localizar clientes específicos
- 📈 Observe taxa de conversão por vendedor

### Boas Práticas

- 💬 Personalize a mensagem para cada cliente
- 🎯 Foque nos clientes com maior ticket médio
- ⏰ Ligue em horários apropriados
- 📱 Tenha script de vendas preparado
- ✍️ Registre observações detalhadas

---

## 🐛 Solução de Problemas

### Problema: Não consigo fazer login

**Solução:**
- Verifique se escolheu um vendedor do dropdown
- Senha padrão: `123456`
- Verifique se o servidor está rodando

### Problema: Não aparecem clientes

**Solução:**
- Verifique se há outros vendedores online
- Clique em "Atualizar"
- Verifique se o banco foi populado (mensagem no console)

### Problema: WebSocket desconectado

**Solução:**
- O sistema tenta reconectar automaticamente
- Recarregue a página se persistir
- Verifique conexão de internet

### Problema: Erro ao marcar contato

**Solução:**
- Verifique conexão com servidor
- Tente fazer logout e login novamente
- Veja logs do servidor no terminal

---

## 📈 Próximos Passos

### Melhorias Sugeridas

1. **Integração WhatsApp**
   - Enviar mensagens diretamente
   - Templates de mensagens

2. **Relatórios**
   - Taxa de conversão
   - Ranking de vendedores
   - Exportar para Excel

3. **Metas**
   - Definir metas diárias
   - Gamificação
   - Recompensas

4. **Notificações**
   - Push notifications
   - Email de lembrete
   - SMS para clientes

5. **Analytics**
   - Dashboard do gestor
   - Gráficos de performance
   - Previsões com IA

---

## 📞 Suporte

### Recursos

- 📖 **README.md** - Documentação completa
- 📚 **http://localhost:8000/docs** - API Docs
- 💻 **Código Fonte** - Comentado e organizado

### Contato

Para dúvidas ou sugestões:
1. Revise este guia
2. Confira o README.md
3. Verifique logs do servidor
4. Analise o código fonte

---

**✨ Desenvolvido com FastAPI, SQLite e tecnologias modernas**

**🎯 Sistema pronto para uso em produção com ajustes de segurança**
