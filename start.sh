#!/bin/bash

# Script para iniciar o CRM Kanban

echo "🚀 Iniciando CRM Kanban..."
echo ""

# Verificar se o Python está instalado
if ! command -v python &> /dev/null
then
    echo "❌ Python não encontrado. Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

# Verificar se as dependências estão instaladas
if ! python -c "import fastapi" &> /dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
fi

# Iniciar o servidor
echo "✅ Iniciando servidor..."
echo ""
echo "🌐 Acesse o sistema em: http://localhost:8000"
echo ""
echo "👥 Vendedores disponíveis:"
echo "   - João Silva"
echo "   - Maria Santos"
echo "   - Pedro Oliveira"
echo "   - Ana Costa"
echo "   - Carlos Ferreira"
echo ""
echo "� Administrador:"
echo "   - Admin (admin123)"
echo ""
echo "🔑 Senha dos vendedores: 123456"
echo ""
echo "📝 Pressione CTRL+C para parar o servidor"
echo ""

python app.py
