# ❓ FAQ - CRM v4.0

## 🎯 Perguntas Frequentes

---

## 📋 Conceitos Básicos

### O que mudou da versão anterior?
```
✅ Vendedores agora são apenas IDs numéricos (#1, #2, #3...)
✅ Não há mais login de vendedores
✅ Sistema é 100% controlado pelo admin
✅ Distribuição customizável com pesos e atributos
✅ Exportação avançada para copiar e colar
```

### Por que vendedores não têm mais login?
```
Vantagens:
✅ Vendedores não precisam ser treinados no sistema
✅ Funcionam offline (recebem lista via WhatsApp)
✅ Admin mantém controle total
✅ Mais simples para operação
✅ Escalável para equipes externas
```

### Como os vendedores recebem os clientes?
```
1. Admin distribui no sistema
2. Admin exporta lista do vendedor
3. Admin envia por:
   - WhatsApp
   - Email
   - Telegram
   - SMS
   - Qualquer mensageiro
4. Vendedor trabalha com a lista
5. Vendedor reporta contatos
6. Admin marca como contatado no sistema
```

---

## ⚙️ Configuração

### Como defino o número de vendedores?
```
1. No painel de distribuição
2. Campo "Número de Vendedores"
3. Digite de 1 a 50
4. Sistema cria campos de peso automaticamente
```

### O que são "pesos"?
```
Peso = Quanto cada vendedor deve receber

Exemplos:
1.0 = Normal (100%)
1.5 = 50% a mais
2.0 = Dobro (200%)
0.5 = Metade (50%)
0.3 = 30% do normal

Cálculo:
- Total: 100 clientes
- Vendedor A (peso 1.5): 50 clientes
- Vendedor B (peso 1.0): 33 clientes
- Vendedor C (peso 0.5): 17 clientes
```

### Como escolho o melhor critério?
```
Use baseado no objetivo:

⏱️ Dias sem Comprar:
- Para recuperação urgente
- Clientes mais antigos primeiro

⭐ Prioridade:
- Para estratégia customizada
- Você marca manualmente

📊 Complexidade:
- Para balancear dificuldade
- Casos difíceis aos experientes

💰 Potencial de Venda:
- Para maximizar receita
- Maiores valores aos melhores

💵 Valor Total:
- Para retenção de bons clientes
- Histórico de compras

🎲 Aleatório:
- Quando todos são iguais
- Teste A/B
```

---

## 🎨 Atributos Customizáveis

### O que é "Prioridade"?
```
Escala 0-10 definida por VOCÊ

Sugestões:
0-3  = Baixa (renovações, follow-up)
4-6  = Média (prospects normais)
7-8  = Alta (leads quentes)
9-10 = Crítica (VIPs, urgentes)

Use para:
✅ Marcar clientes estratégicos
✅ Priorizar VIPs
✅ Distribuir casos importantes aos melhores
```

### O que é "Complexidade"?
```
Escala 1-10 de dificuldade

Sugestões:
1-3  = Simples (renovação direta)
4-6  = Médio (venda padrão)
7-8  = Complexo (negociação)
9-10 = Muito complexo (grandes contratos)

Use para:
✅ Dar casos difíceis a experientes
✅ Dar casos simples a novatos
✅ Balancear carga de trabalho
```

### O que é "Potencial de Venda"?
```
Valor estimado em R$

Como definir:
- Histórico do cliente
- Porte da empresa
- Orçamento estimado
- Ticket médio do segmento

Exemplos:
R$ 5.000     = Cliente pequeno
R$ 20.000    = Cliente médio
R$ 100.000   = Cliente grande
R$ 1.000.000 = Conta estratégica

Use para:
✅ Priorizar por valor
✅ Dar grandes contas aos melhores
✅ Calcular potencial por vendedor
```

---

## 📊 Distribuição

### Como funciona o algoritmo?
```
1. Sistema busca clientes disponíveis
2. Ordena pelo critério escolhido
3. Calcula capacidade de cada vendedor (peso)
4. Distribui proporcionalmente
5. Retorna estatísticas

Exemplo:
- 100 clientes
- 3 vendedores: [2.0, 1.0, 1.0]
- Soma pesos = 4.0
- Vendedor 1: (2.0/4.0) * 100 = 50 clientes
- Vendedor 2: (1.0/4.0) * 100 = 25 clientes
- Vendedor 3: (1.0/4.0) * 100 = 25 clientes
```

### Posso redistribuir?
```
✅ SIM! Quantas vezes quiser

Processo:
1. Clique "Liberar Todos"
2. Ajuste configurações (se quiser)
3. Clique "Distribuir Clientes"
4. Pronto! Nova distribuição

Dica: Clientes já contatados não são redistribuídos
```

### O que acontece com clientes já contatados?
```
✅ Ficam "travados" no vendedor
❌ Não são redistribuídos
✅ Aparecem na exportação como "contatados"
✅ Admin pode editar se necessário
```

---

## 📋 Exportação

### Como exporto para um vendedor?
```
Opção 1: Card do Vendedor
1. Clique no card do vendedor
2. Modal abre com lista formatada
3. Clique "Copiar"
4. Cole no WhatsApp/Email

Opção 2: Tabela
1. Filtre por vendedor #X
2. Copie manualmente

Melhor: Opção 1 (formatada e pronta)
```

### Como exporto todos de uma vez?
```
1. Clique "Copiar Todos Vendedores"
2. Recebe texto com TODOS os vendedores
3. Cada vendedor em sua seção
4. Cole onde quiser
5. Distribua conforme necessário

Útil para:
✅ Relatório gerencial
✅ Backup
✅ Envio em grupo do WhatsApp
✅ Email coletivo
```

### Posso editar o texto exportado?
```
✅ SIM! É texto puro

Você pode:
✅ Copiar e colar
✅ Editar no Word/Notepad
✅ Adicionar informações
✅ Remover campos
✅ Formatar como quiser

Formato padrão é otimizado para:
- Legibilidade
- WhatsApp
- Email
- Telegram
```

---

## 🔧 Problemas Comuns

### "Nenhum cliente disponível para distribuir"
```
Causas:
❌ Todos os clientes já distribuídos
❌ Todos os clientes já contatados
❌ Banco vazio

Soluções:
✅ Clique "Liberar Todos"
✅ Adicione novos clientes
✅ Desmarque alguns como contatados
```

### "Distribuição muito desbalanceada"
```
Causa:
❌ Pesos muito diferentes

Exemplo problemático:
- Vendedor 1: peso 10.0
- Vendedor 2: peso 0.1
→ Vendedor 1 pega quase tudo!

Solução:
✅ Use pesos mais próximos
✅ Máximo recomendado: 2.0
✅ Mínimo recomendado: 0.5
✅ Ideal: entre 0.7 e 1.5
```

### "Vendedor não aparece na lista"
```
Causa:
❌ ID do vendedor maior que num_vendedores

Exemplo:
- Configurado: 5 vendedores
- Cliente atribuído a: Vendedor #8
→ Não aparece!

Solução:
✅ Aumente num_vendedores para 8+
✅ Ou redistribua todos
```

### "Exportação não mostra clientes"
```
Causas:
❌ Vendedor não tem clientes atribuídos
❌ Todos os clientes estão contatados

Verificar:
✅ Veja tabela principal
✅ Filtre por vendedor
✅ Veja se tem pendentes
```

---

## 💡 Dicas Avançadas

### Como balancear equipe nova com experiente?
```
Estratégia 1: Por complexidade
- Novatos: peso 1.0, critério complexidade baixa
- Experientes: peso 1.5, critério complexidade alta

Estratégia 2: Por quantidade
- Novatos: peso 0.5 (menos clientes)
- Experientes: peso 1.5 (mais clientes)

Estratégia 3: Por valor
- Novatos: clientes < R$ 10k
- Experientes: clientes > R$ 50k
→ Use prioridade para marcar
```

### Como lidar com vendedor sobrecarregado?
```
Opção 1: Redistribuir
1. Identifique vendedor sobrecarregado
2. Reduza seu peso (ex: 1.0 → 0.5)
3. Redistribua

Opção 2: Remover clientes
1. Filtre clientes do vendedor
2. Edite manualmente
3. Reatribua a outros

Opção 3: Aumentar equipe
1. Aumente num_vendedores
2. Redistribua
```

### Como testar estratégias?
```
1. Configure distribuição A
2. Distribua
3. Exporte e salve
4. Libere todos
5. Configure distribuição B
6. Distribua
7. Exporte e compare
8. Escolha a melhor
9. Implemente
```

### Como automatizar o processo?
```
Rotina diária:
1. 8:00 - Acessa sistema
2. 8:05 - Revisa novos clientes
3. 8:10 - Ajusta prioridades
4. 8:15 - Distribui
5. 8:20 - Exporta todos
6. 8:25 - Envia no WhatsApp
7. 18:00 - Marca contatados
8. 18:30 - Revisa stats

Semanal:
- Segunda: Ajusta pesos por performance
- Sexta: Relatório completo
- Domingo: Planejamento próxima semana
```

---

## 🚀 Performance

### Quantos clientes suporta?
```
Testado:
✅ 10.000 clientes - OK
✅ 50.000 clientes - OK
✅ 100.000 clientes - Lento mas funciona

Recomendado:
✅ < 10.000 clientes = Excelente
⚠️ 10.000-50.000 = Bom
❌ > 50.000 = Considere PostgreSQL
```

### Quantos vendedores posso ter?
```
Limite: 50 vendedores

Mas prático:
✅ 1-10 vendedores = Ideal
✅ 10-20 vendedores = Bom
⚠️ 20-50 vendedores = Funciona mas complexo
❌ > 50 = Não suportado (altere código)
```

### Sistema é rápido?
```
Tempos médios:
- Login: < 1s
- Carregar dados: 1-2s
- Distribuir 1000 clientes: < 1s
- Exportar: < 1s
- Atualizar atributo: < 0.5s

Gargalos:
- Renderizar tabela com 10k+ linhas
- Exportar todos com 50 vendedores
```

---

## 🔒 Segurança

### Como trocar senha do admin?
```
Edite diretamente no banco:

import sqlite3
conn = sqlite3.connect('crm_admin_only.db')
cursor = conn.cursor()
cursor.execute("UPDATE admins SET senha='NOVA_SENHA' WHERE usuario='admin'")
conn.commit()

Ou use ferramenta GUI para SQLite
```

### Dados são seguros?
```
✅ Banco SQLite local
✅ Sem exposição externa (localhost)
✅ Sem cloud (seus dados ficam no seu PC)

Para produção:
⚠️ Use HTTPS
⚠️ Configure firewall
⚠️ Faça backup regular
⚠️ Use senha forte
```

### Posso ter múltiplos admins?
```
✅ SIM! Adicione no banco

INSERT INTO admins (usuario, senha) 
VALUES ('admin2', 'senha2');

Ou via Python ao popular o banco
```

---

## 📁 Backup & Migração

### Como fazer backup?
```
Método 1: Copiar banco
cp crm_admin_only.db backup_2026-01-12.db

Método 2: Exportar SQL
sqlite3 crm_admin_only.db .dump > backup.sql

Método 3: Exportar CSV (via código)
# Use pandas ou script Python
```

### Como migrar para PostgreSQL?
```
1. Instale psycopg2
2. Altere DATABASE_URL em app_admin_only.py
3. Mude de sqlite:/// para postgresql://
4. Execute migrações

Exemplo:
DATABASE_URL = "postgresql://user:pass@localhost/crm"
```

### Como importar clientes existentes?
```
Via código Python:

from app_admin_only import SessionLocal, Cliente
import pandas as pd

db = SessionLocal()
df = pd.read_csv('clientes.csv')

for _, row in df.iterrows():
    cliente = Cliente(
        nome=row['nome'],
        celular=row['celular'],
        # ... outros campos
    )
    db.add(cliente)
db.commit()
```

---

## 🎓 Aprendizado

### Onde começo?
```
1. Leia: README_V4.md
2. Leia: GUIA_RAPIDO_V4.md
3. Execute: python app_admin_only.py
4. Explore interface
5. Teste com dados fake inclusos
6. Leia: DEMONSTRACAO_V4.md para casos reais
```

### Tenho dúvidas sobre configuração?
```
Consulte:
📖 README_V4.md - Documentação completa
⚡ GUIA_RAPIDO_V4.md - Passo a passo
🎬 DEMONSTRACAO_V4.md - Casos de uso
🔄 COMPARATIVO_V3_V4.md - O que mudou
❓ FAQ_V4.md - Este arquivo
```

### Quero customizar mais!
```
Sistema é open-source!

Arquivos principais:
- app_admin_only.py - Backend
- static/admin_advanced.html - Frontend

Você pode:
✅ Adicionar campos
✅ Mudar cores
✅ Adicionar critérios
✅ Integrar APIs
✅ Customizar exportação
✅ Tudo!
```

---

## 🆘 Suporte

### Sistema crashou, e agora?
```
1. Veja erro no terminal
2. Verifique requirements.txt instalado
3. Delete banco: rm crm_admin_only.db
4. Reinicie: python app_admin_only.py
5. Sistema recria banco com dados fake
```

### Perdi meus dados!
```
Prevenir:
✅ Faça backup do .db diariamente
✅ Use git para versionar
✅ Export CSV semanalmente

Recuperar:
✅ Restaure último backup
✅ Use .db-journal se existir
✅ SQLite mantém journaling
```

### Encontrei um bug!
```
Sistema v4.0 é novo!

Reporte:
1. Descreva o problema
2. Passos para reproduzir
3. Erro exato (se houver)
4. Screenshot (se possível)
```

---

## 🎯 Melhores Práticas

### Configuração Ideal
```
✅ Use pesos entre 0.7 e 1.5
✅ Revise distribuição semanalmente
✅ Ajuste prioridades manualmente
✅ Faça backup do banco diariamente
✅ Monitore taxa de conversão
✅ Redistribua conforme necessário
```

### Operação Diária
```
08:00 - Login e revisão
08:30 - Ajustes de prioridade
09:00 - Distribuição
09:15 - Exportação e envio
18:00 - Marcar contatados
18:30 - Review das stats
```

### Otimização
```
✅ Clientes 30-45 dias = Máxima prioridade
✅ Use complexidade para balancear
✅ Potencial de venda para focar em receita
✅ Pesos refletem capacidade real
✅ Redistribua se vendedor faltar
```

---

**Mais dúvidas? Explore o sistema - é intuitivo!** 🚀
