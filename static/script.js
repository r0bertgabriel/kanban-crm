// Estado Global
let currentUser = null;
let ws = null;
let clientesList = [];

// Elementos DOM
const loginScreen = document.getElementById('loginScreen');
const dashboardScreen = document.getElementById('dashboardScreen');
const loginForm = document.getElementById('loginForm');
const logoutBtn = document.getElementById('logoutBtn');
const userName = document.getElementById('userName');
const clientesListEl = document.getElementById('clientesList');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const refreshBtn = document.getElementById('refreshBtn');
const contatoModal = document.getElementById('contatoModal');
const vendedoresListEl = document.getElementById('vendedoresList');
const onlineCount = document.getElementById('onlineCount');

// Formatação
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value / 100);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Hoje';
    if (diffDays === 1) return 'Ontem';
    return `${diffDays} dias atrás`;
}

function formatPhone(phone) {
    // Remove +55 e formata (XX) 9XXXX-XXXX
    const cleaned = phone.replace('+55', '');
    const match = cleaned.match(/^(\d{2})(\d{5})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

// Login
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('loginError');
    
    // Validar seleção
    if (username === '' || username === '── Vendedores ──') {
        errorEl.textContent = 'Por favor, selecione um usuário válido';
        return;
    }
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome: username, senha: password })
        });
        
        if (!response.ok) {
            throw new Error('Credenciais inválidas');
        }
        
        const data = await response.json();
        currentUser = data;
        
        // Redirecionar admin para painel de admin
        if (data.is_admin) {
            window.location.href = '/admin';
            return;
        }
        
        // Mudar para tela do dashboard
        loginScreen.classList.remove('active');
        dashboardScreen.classList.add('active');
        userName.textContent = currentUser.nome;
        
        // Conectar WebSocket
        connectWebSocket();
        
        // Carregar dados
        loadDashboard();
        
    } catch (error) {
        errorEl.textContent = error.message;
    }
});

// Logout
logoutBtn.addEventListener('click', async () => {
    if (confirm('Deseja realmente sair?')) {
        try {
            await fetch(`/api/auth/logout/${currentUser.id}`, { method: 'POST' });
            
            if (ws) {
                ws.close();
            }
            
            currentUser = null;
            dashboardScreen.classList.remove('active');
            loginScreen.classList.add('active');
            
            // Limpar formulário
            document.getElementById('loginError').textContent = '';
        } catch (error) {
            console.error('Erro ao fazer logout:', error);
        }
    }
});

// WebSocket
function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/${currentUser.id}`);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.tipo === 'cliente_contatado') {
            // Recarregar lista de clientes
            loadClientes();
            loadEstatisticas();
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        console.log('WebSocket desconectado');
        // Tentar reconectar após 3 segundos
        if (currentUser) {
            setTimeout(connectWebSocket, 3000);
        }
    };
}

// Carregar Dashboard
async function loadDashboard() {
    await Promise.all([
        loadVendedores(),
        loadClientes(),
        loadEstatisticas()
    ]);
}

// Carregar Vendedores
async function loadVendedores() {
    try {
        const response = await fetch('/api/auth/vendedores');
        const vendedores = await response.json();
        
        const online = vendedores.filter(v => v.online);
        onlineCount.textContent = online.length;
        
        vendedoresListEl.innerHTML = vendedores.map(v => `
            <div class="vendedor-badge ${v.online ? 'online' : 'offline'}">
                ${v.online ? '<span class="vendedor-dot"></span>' : ''}
                ${v.nome}
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Erro ao carregar vendedores:', error);
    }
}

// Carregar Clientes
async function loadClientes() {
    try {
        const response = await fetch(`/api/vendedor/meus-clientes/${currentUser.id}`);
        clientesList = await response.json();
        
        renderClientes(clientesList);
        
    } catch (error) {
        console.error('Erro ao carregar clientes:', error);
    }
}

// Renderizar Clientes
function renderClientes(clientes) {
    if (clientes.length === 0) {
        clientesListEl.innerHTML = '';
        emptyState.classList.add('show');
        return;
    }
    
    emptyState.classList.remove('show');
    
    clientesListEl.innerHTML = clientes.map(cliente => {
        let badgeClass = 'badge-warning';
        let badgeText = '⚠️ Inativo';
        
        if (cliente.dias_sem_comprar <= 45) {
            badgeClass = 'badge-danger';
            badgeText = '🔥 Urgente';
        }
        
        return `
        <div class="cliente-card" data-id="${cliente.id}">
            <div class="cliente-header">
                <div>
                    <div class="cliente-nome">${cliente.nome}</div>
                </div>
                <span class="badge ${badgeClass}">${badgeText}</span>
            </div>
            
            <div class="cliente-info">
                <div class="info-item">
                    📱 <strong>${formatPhone(cliente.celular)}</strong>
                </div>
                <div class="info-item">
                    📧 ${cliente.email}
                </div>
                <div class="info-item">
                    🕒 Última compra: <strong>${cliente.dias_sem_comprar} dias atrás</strong>
                </div>
            </div>
            
            <div class="cliente-stats">
                <div class="stat-item">
                    <div class="stat-label">Ticket Total</div>
                    <div class="stat-value">${formatCurrency(cliente.valor_total_compras)}</div>
                </div>
            </div>
            
            <div class="cliente-actions">
                <button class="btn btn-success btn-contact" onclick="abrirModalContato(${cliente.id})">
                    ✅ Marcar como Contatado
                </button>
            </div>
        </div>
    `;
    }).join('');
}

// Carregar Estatísticas
async function loadEstatisticas() {
    try {
        const response = await fetch(`/api/vendedor/estatisticas/${currentUser.id}`);
        const stats = await response.json();
        
        document.getElementById('statPendentes').textContent = stats.total_pendentes;
        document.getElementById('statContatados').textContent = stats.total_contatados;
        document.getElementById('statTotal').textContent = stats.total_atribuidos;
        
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

// Buscar Clientes
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    
    if (query === '') {
        renderClientes(clientesList);
        return;
    }
    
    const filtered = clientesList.filter(cliente => 
        cliente.nome.toLowerCase().includes(query) ||
        cliente.celular.includes(query) ||
        cliente.email.toLowerCase().includes(query)
    );
    
    renderClientes(filtered);
});

// Refresh
refreshBtn.addEventListener('click', () => {
    refreshBtn.textContent = '🔄 Atualizando...';
    refreshBtn.disabled = true;
    
    loadDashboard().finally(() => {
        refreshBtn.textContent = '🔄 Atualizar';
        refreshBtn.disabled = false;
    });
});

// Modal de Contato
let clienteContatoId = null;

function abrirModalContato(clienteId) {
    clienteContatoId = clienteId;
    const cliente = clientesList.find(c => c.id === clienteId);
    
    if (!cliente) return;
    
    document.getElementById('modalClienteNome').textContent = cliente.nome;
    document.getElementById('modalClienteCelular').textContent = formatPhone(cliente.celular);
    document.getElementById('observacoes').value = '';
    
    contatoModal.classList.add('active');
}

function closeModal() {
    contatoModal.classList.remove('active');
    clienteContatoId = null;
}

async function confirmarContato() {
    const observacoes = document.getElementById('observacoes').value;
    
    try {
        const response = await fetch(`/api/vendedor/marcar-contatado/${currentUser.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cliente_id: clienteContatoId,
                observacoes: observacoes || null
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao marcar cliente');
        }
        
        // Fechar modal
        closeModal();
        
        // Recarregar dados
        await loadClientes();
        await loadEstatisticas();
        
        // Mostrar feedback
        showNotification('✅ Cliente marcado como contatado!');
        
    } catch (error) {
        console.error('Erro ao marcar contato:', error);
        alert('Erro ao marcar cliente como contatado. Tente novamente.');
    }
}

// Notificação
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        background: #10b981;
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
contatoModal.addEventListener('click', (e) => {
    if (e.target === contatoModal) {
        closeModal();
    }
});

// Animations CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// Auto-refresh a cada 30 segundos
setInterval(() => {
    if (currentUser) {
        loadVendedores();
    }
}, 30000);
