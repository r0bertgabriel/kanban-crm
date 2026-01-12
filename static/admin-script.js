// Estado Global
let todosClientes = [];
let vendedores = [];
let clienteRealocacaoId = null;

// Elementos DOM
const logoutBtn = document.getElementById('logoutBtn');
const redistribuirBtn = document.getElementById('redistribuirBtn');
const realocacaoModal = document.getElementById('realocacaoModal');

// Formatação
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value / 100);
}

function formatPhone(phone) {
    const cleaned = phone.replace('+55', '');
    const match = cleaned.match(/^(\d{2})(\d{5})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

// Logout
logoutBtn.addEventListener('click', () => {
    if (confirm('Deseja sair do painel administrativo?')) {
        window.location.href = '/';
    }
});

// Redistribuir Todos
redistribuirBtn.addEventListener('click', async () => {
    if (confirm('Deseja redistribuir TODOS os clientes entre os vendedores online?')) {
        redistribuirBtn.disabled = true;
        redistribuirBtn.textContent = '🔄 Redistribuindo...';
        
        try {
            await fetch('/api/admin/redistribuir-todos', { method: 'POST' });
            showNotification('✅ Clientes redistribuídos com sucesso!');
            loadDashboard();
        } catch (error) {
            console.error('Erro ao redistribuir:', error);
            showNotification('❌ Erro ao redistribuir clientes', 'error');
        } finally {
            redistribuirBtn.disabled = false;
            redistribuirBtn.textContent = '🔄 Redistribuir Todos';
        }
    }
});

// Carregar Dashboard
async function loadDashboard() {
    await Promise.all([
        loadEstatisticas(),
        loadClientesPorPeriodo(),
        loadTodosClientes(),
        loadPerformanceVendedores(),
        loadVendedores()
    ]);
}

// Carregar Estatísticas
async function loadEstatisticas() {
    try {
        const response = await fetch('/api/admin/estatisticas-gerais');
        const stats = await response.json();
        
        document.getElementById('totalClientes').textContent = stats.total_clientes;
        document.getElementById('clientes3060').textContent = stats.clientes_30_60_dias;
        document.getElementById('clientesDisponiveis').textContent = stats.clientes_disponiveis;
        document.getElementById('clientesContatados').textContent = stats.clientes_contatados;
        document.getElementById('vendedoresOnline').textContent = stats.vendedores_online;
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Carregar Clientes por Período
async function loadClientesPorPeriodo() {
    try {
        const response = await fetch('/api/admin/clientes-por-periodo');
        const periodos = await response.json();
        
        renderClientesPeriodo('30_45_dias', periodos['30_45_dias'], 'clientes30_45');
        renderClientesPeriodo('45_60_dias', periodos['45_60_dias'], 'clientes45_60');
        renderClientesPeriodo('60_90_dias', periodos['60_90_dias'], 'clientes60_90');
        renderClientesPeriodo('mais_90_dias', periodos['mais_90_dias'], 'clientesMais90');
    } catch (error) {
        console.error('Erro ao carregar clientes por período:', error);
    }
}

function renderClientesPeriodo(periodo, clientes, elementId) {
    const container = document.getElementById(elementId);
    
    if (!clientes || clientes.length === 0) {
        container.innerHTML = '<div class="loading">Nenhum cliente neste período</div>';
        return;
    }
    
    container.innerHTML = clientes.map(cliente => `
        <div class="cliente-mini-card">
            <div class="cliente-mini-header">
                <span class="cliente-mini-nome">${cliente.nome}</span>
                <span class="cliente-mini-dias">${cliente.dias_sem_comprar}d</span>
            </div>
            <div class="cliente-mini-info">📱 ${formatPhone(cliente.celular)}</div>
            <div class="cliente-mini-info">💰 ${formatCurrency(cliente.valor_total_compras)}</div>
            ${cliente.vendedor_atribuido ? 
                `<div class="cliente-mini-vendedor">👤 ${cliente.vendedor_atribuido}</div>` : 
                `<div class="cliente-mini-disponivel">⚠️ Disponível</div>`
            }
        </div>
    `).join('');
}

// Carregar Todos os Clientes
async function loadTodosClientes() {
    try {
        const response = await fetch('/api/admin/todos-clientes');
        todosClientes = await response.json();
        renderTodosClientes(todosClientes);
    } catch (error) {
        console.error('Erro ao carregar todos os clientes:', error);
    }
}

function renderTodosClientes(clientes) {
    const tbody = document.getElementById('todosClientesList');
    
    if (!clientes || clientes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading">Nenhum cliente encontrado</td></tr>';
        return;
    }
    
    tbody.innerHTML = clientes.map(cliente => `
        <tr>
            <td>
                <strong>${cliente.nome}</strong><br>
                <small style="color: var(--text-secondary)">${cliente.email}</small>
            </td>
            <td>${formatPhone(cliente.celular)}</td>
            <td>
                <strong style="color: ${cliente.dias_sem_comprar > 60 ? 'var(--danger)' : 'var(--warning)'}">
                    ${cliente.dias_sem_comprar} dias
                </strong>
            </td>
            <td>${formatCurrency(cliente.valor_total_compras)}</td>
            <td>
                <span class="status-badge status-${cliente.status}">
                    ${cliente.status}
                </span>
            </td>
            <td>${cliente.vendedor_atribuido || '-'}</td>
            <td class="table-actions">
                ${!cliente.contatado ? `
                    <button class="btn btn-small btn-primary" onclick="abrirModalRealocacao(${cliente.id})">
                        🔄 Realocar
                    </button>
                    <button class="btn btn-small btn-secondary" onclick="liberarCliente(${cliente.id})">
                        🔓 Liberar
                    </button>
                ` : `
                    <span style="color: var(--success); font-size: 12px;">✅ Contatado</span>
                `}
            </td>
        </tr>
    `).join('');
}

// Buscar Clientes
document.getElementById('searchClientes').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    
    if (query === '') {
        renderTodosClientes(todosClientes);
        return;
    }
    
    const filtered = todosClientes.filter(cliente => 
        cliente.nome.toLowerCase().includes(query) ||
        cliente.celular.includes(query) ||
        cliente.email.toLowerCase().includes(query)
    );
    
    renderTodosClientes(filtered);
});

// Carregar Performance dos Vendedores
async function loadPerformanceVendedores() {
    try {
        const response = await fetch('/api/admin/estatisticas-gerais');
        const stats = await response.json();
        
        const container = document.getElementById('vendedoresPerformance');
        
        if (!stats.performance_vendedores || stats.performance_vendedores.length === 0) {
            container.innerHTML = '<div class="loading">Nenhum vendedor cadastrado</div>';
            return;
        }
        
        container.innerHTML = stats.performance_vendedores.map(vendedor => `
            <div class="vendedor-performance-card">
                <div class="vendedor-performance-header">
                    <span class="vendedor-performance-nome">${vendedor.nome}</span>
                    <span class="vendedor-performance-online ${vendedor.online ? 'online' : 'offline'}">
                        ${vendedor.online ? '🟢 Online' : '⚪ Offline'}
                    </span>
                </div>
                <div class="vendedor-performance-stats">
                    <div class="performance-stat">
                        <div class="performance-stat-value">${vendedor.total_atribuidos}</div>
                        <div class="performance-stat-label">Atribuídos</div>
                    </div>
                    <div class="performance-stat">
                        <div class="performance-stat-value">${vendedor.total_contatados}</div>
                        <div class="performance-stat-label">Contatados</div>
                    </div>
                </div>
                <div class="vendedor-taxa-conversao">
                    <div class="taxa-conversao-value">${vendedor.taxa_conversao}%</div>
                    <div class="taxa-conversao-label">Taxa de Conversão</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar performance:', error);
    }
}

// Carregar Lista de Vendedores (para modal)
async function loadVendedores() {
    try {
        const response = await fetch('/api/auth/vendedores');
        vendedores = await response.json();
    } catch (error) {
        console.error('Erro ao carregar vendedores:', error);
    }
}

// Modal de Realocação
function abrirModalRealocacao(clienteId) {
    clienteRealocacaoId = clienteId;
    const cliente = todosClientes.find(c => c.id === clienteId);
    
    if (!cliente) return;
    
    document.getElementById('modalClienteNome').textContent = cliente.nome;
    document.getElementById('modalClienteInfo').textContent = 
        `${formatPhone(cliente.celular)} | ${cliente.dias_sem_comprar} dias sem comprar`;
    
    // Preencher select de vendedores
    const select = document.getElementById('selectVendedor');
    select.innerHTML = '<option value="">Selecione um vendedor</option>' +
        vendedores.map(v => `
            <option value="${v.id}">
                ${v.nome} ${v.online ? '🟢' : '⚪'}
            </option>
        `).join('');
    
    realocacaoModal.classList.add('active');
}

function closeRealocacaoModal() {
    realocacaoModal.classList.remove('active');
    clienteRealocacaoId = null;
}

async function confirmarRealocacao() {
    const vendedorId = document.getElementById('selectVendedor').value;
    
    if (!vendedorId) {
        alert('Selecione um vendedor');
        return;
    }
    
    try {
        const response = await fetch('/api/admin/realocar-cliente', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cliente_id: clienteRealocacaoId,
                vendedor_id: parseInt(vendedorId)
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao realocar');
        }
        
        closeRealocacaoModal();
        showNotification('✅ Cliente realocado com sucesso!');
        loadDashboard();
    } catch (error) {
        console.error('Erro ao realocar:', error);
        showNotification('❌ Erro ao realocar cliente', 'error');
    }
}

// Liberar Cliente
async function liberarCliente(clienteId) {
    if (!confirm('Deseja liberar este cliente? Ele ficará disponível para redistribuição.')) {
        return;
    }
    
    try {
        await fetch(`/api/admin/liberar-cliente/${clienteId}`, { method: 'POST' });
        showNotification('✅ Cliente liberado com sucesso!');
        loadDashboard();
    } catch (error) {
        console.error('Erro ao liberar cliente:', error);
        showNotification('❌ Erro ao liberar cliente', 'error');
    }
}

// Switch Tabs
function switchTab(tabName) {
    // Remover active de todas as tabs
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    // Ativar tab selecionada
    if (tabName === 'periodos') {
        document.querySelector('.tab:nth-child(1)').classList.add('active');
        document.getElementById('tabPeriodos').classList.add('active');
    } else if (tabName === 'todos') {
        document.querySelector('.tab:nth-child(2)').classList.add('active');
        document.getElementById('tabTodos').classList.add('active');
    } else if (tabName === 'vendedores') {
        document.querySelector('.tab:nth-child(3)').classList.add('active');
        document.getElementById('tabVendedores').classList.add('active');
    }
}

// Notificação
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Fechar modal ao clicar fora
realocacaoModal.addEventListener('click', (e) => {
    if (e.target === realocacaoModal) {
        closeRealocacaoModal();
    }
});

// Auto-refresh a cada 30 segundos
setInterval(loadDashboard, 30000);

// Carregar dados inicial
loadDashboard();
