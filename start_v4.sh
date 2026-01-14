#!/bin/bash

echo "🚀 Iniciando Painel Vendedor - Sistema Admin Only"
echo "================================================"
echo ""
echo "📋 Verificando dependências..."

# Instalar dependências se necessário
pip install -q -r requirements.txt

echo "✅ Dependências instaladas"
echo ""
echo "🗄️  Inicializando banco de dados..."
echo ""
echo "🌐 Iniciando servidor..."
echo ""
echo "================================================"
echo "🎯 Sistema pronto!"
echo "📍 Acesse: http://localhost:8000"
echo "👤 Login: admin / admin123"
echo "================================================"
echo ""

# Executar aplicação
python app_admin_only.py
