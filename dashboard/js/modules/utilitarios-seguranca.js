// ============================================================
    // UTILITÁRIOS DE SEGURANÇA
    // ============================================================
    /**
     * Escapa caracteres HTML para prevenir XSS.
     * Deve ser usada em TODA interpolação de dados dinâmicos no DOM.
     */
    function escapeHtml(str) {
        if (str == null) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    /**
     * Toast genérico reutilizável — substitui as 4 implementações duplicadas.
     * @param {string} msg - Mensagem (já escaped ou texto puro)
     * @param {'success'|'warning'|'error'|'info'} variant
     * @param {number} duration - Duração em ms (padrão 3000)
     */
    const _toastIcons = { success: '✓', warning: '⚠', error: '✕', info: 'ℹ' };
    const _toastColors = {
        success: { bg: '#D1FAE5', color: '#065F46', border: '#10B981' },
        warning: { bg: '#FEF3C7', color: '#92400E', border: '#F59E0B' },
        error:   { bg: '#FEE2E2', color: '#991B1B', border: '#DC2626' },
        info:    { bg: '#DBEAFE', color: '#1E40AF', border: '#0EA5E9' }
    };
    let _activeToastTimer = null;
    function showToast(msg, variant, duration) {
        variant = variant || 'success';
        duration = duration || 3000;
        const c = _toastColors[variant] || _toastColors.info;
        let toast = document.getElementById('ucgs-global-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'ucgs-global-toast';
            toast.setAttribute('role', 'status');
            toast.setAttribute('aria-live', 'polite');
            Object.assign(toast.style, {
                position: 'fixed', bottom: '24px', right: '24px', zIndex: '9999',
                padding: '14px 22px', borderRadius: '10px', fontFamily: 'Inter, system-ui, sans-serif',
                fontSize: '0.875rem', fontWeight: '600', display: 'flex', alignItems: 'center',
                gap: '10px', boxShadow: '0 8px 24px rgba(0,0,0,0.15)', opacity: '0',
                transform: 'translateY(12px)', transition: 'all 0.3s ease', pointerEvents: 'none'
            });
            document.body.appendChild(toast);
        }
        clearTimeout(_activeToastTimer);
        toast.textContent = '';
        const icon = document.createElement('span');
        icon.textContent = _toastIcons[variant] || '✓';
        icon.style.fontSize = '1rem';
        const text = document.createElement('span');
        text.textContent = msg;
        toast.appendChild(icon);
        toast.appendChild(text);
        Object.assign(toast.style, {
            background: c.bg, color: c.color, borderLeft: '4px solid ' + c.border,
            opacity: '1', transform: 'translateY(0)'
        });
        _activeToastTimer = setTimeout(function() {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(12px)';
        }, duration);
    }

    // ============================================================
    // NAVIGATION (refatorada — event delegation + cache de queries)
    // ============================================================
    const _navItems = document.querySelectorAll('.nav-item');
    const _contentSections = document.querySelectorAll('.content-section');

    document.querySelector('.sidebar').addEventListener('click', function(e) {
        const item = e.target.closest('.nav-item');
        if (!item) return;

        const section = item.getAttribute('data-section');

        // Atendimento Médico opens as full-screen overlay instead of content section
        if (section === 'atendimento-medico') {
            _navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            if (typeof atdOpen === 'function') atdOpen();
            return;
        }
        _navItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        _contentSections.forEach(s => s.classList.remove('active'));
        const targetSection = document.getElementById(section);
        if (targetSection) targetSection.classList.add('active');
    });

    document.querySelectorAll('.alert-card').forEach(card => {
        card.addEventListener('click', function() {
            alert('Abrindo detalhes do alerta: ' + this.querySelector('.alert-title').textContent);
        });
    });

    /* Protocol card click handlers moved to Protocol Fullscreen Viewer script */

    // ============================================================
    // NOTIFICATION DATA — simula retorno de API/banco de dados
    // Categorias: vacinas, protocolos | Prioridades: urgente, medio, baixo
    // ============================================================
    const NOTIFICATIONS = [
        {
            id: 1,
            categoria: 'protocolos',
            prioridade: 'urgente',
            titulo: 'Protocolo Perfurocortantes em Atraso',
            descricao: 'Protocolo de acidentes com perfurocortantes venceu em 15/03/2026. Revisão imediata necessária.',
            responsavel: 'Dra. Maria Costa',
            vencimento: '15/03/2026',
            lida: false,
        },
        {
            id: 2,
            categoria: 'protocolos',
            prioridade: 'medio',
            titulo: 'Protocolo Riscos Químicos Pendente',
            descricao: 'Atualização do protocolo de riscos químicos vence em 28/03/2026. Requer revisão dos procedimentos de EPI.',
            responsavel: 'Eng. Carlos Alves',
            vencimento: '28/03/2026',
            lida: false,
        },
        {
            id: 3,
            categoria: 'vacinas',
            prioridade: 'medio',
            titulo: 'Vacinação em Atraso — Detento #235',
            descricao: 'Falta 2ª dose de Hepatite B e reforço de Tétano. Cartão vacinal com pendência há 12 dias.',
            responsavel: 'Enf. Pedro Santos',
            vencimento: '02/04/2026',
            lida: false,
        },
        {
            id: 4,
            categoria: 'vacinas',
            prioridade: 'baixo',
            titulo: 'Campanha Influenza — Aviso Prévio',
            descricao: 'Campanha de vacinação contra Influenza prevista para 05/04/2026. Preparar lista de profissionais.',
            responsavel: 'Guilherme Ferreira',
            vencimento: '05/04/2026',
            lida: true,
        },
    ];

    const PRIORIDADE_LABEL = { urgente: '🔴 Urgente', medio: '🟡 Médio', baixo: '🟢 Baixo' };
    const CATEGORIA_LABEL  = { vacinas: '💉 Vacina', protocolos: '📋 Protocolo' };

    function getRelativeTime(dateStr) {
        const parts = dateStr.split('/');
        const d = new Date(`${parts[2]}-${parts[1]}-${parts[0]}`);
        const now = new Date('2026-03-21');
        const diff = Math.round((d - now) / 86400000);
        if (diff < 0)  return `Venceu há ${Math.abs(diff)} dia(s)`;
        if (diff === 0) return 'Vence hoje!';
        return `Vence em ${diff} dia(s)`;
    }

    let currentFilter = 'all';

    function renderNotifications() {
        const list = document.getElementById('notifList');
        const unread = NOTIFICATIONS.filter(n => !n.lida).length;
        document.getElementById('notifBadge').textContent = unread;
        document.getElementById('notifBadge').style.display = unread ? 'flex' : 'none';
        document.getElementById('notifCountPill').textContent = unread;

        const filtered = NOTIFICATIONS.filter(n => {
            if (currentFilter === 'all') return true;
            if (currentFilter === 'urgente') return n.prioridade === 'urgente';
            return n.categoria === currentFilter;
        });

        if (filtered.length === 0) {
            list.innerHTML = `<div style="padding:40px 24px;text-align:center;color:var(--text-secondary);">
                <div style="font-size:2rem;margin-bottom:12px;">✅</div>
                <div style="font-weight:600;margin-bottom:4px;">Nenhuma notificação</div>
                <div style="font-size:0.85rem;">Tudo em dia nesta categoria.</div>
            </div>`;
            return;
        }

        list.innerHTML = filtered.map(n => `
            <div class="notif-item ${n.lida ? '' : 'unread'}" data-id="${escapeHtml(n.id)}">
                <div class="notif-priority-dot ${escapeHtml(n.prioridade)}"></div>
                <div class="notif-body">
                    <div class="notif-item-header">
                        <span class="notif-tag ${escapeHtml(n.prioridade)}">${escapeHtml(PRIORIDADE_LABEL[n.prioridade])}</span>
                        <span class="notif-time">${escapeHtml(getRelativeTime(n.vencimento))}</span>
                    </div>
                    <div class="notif-title">${escapeHtml(CATEGORIA_LABEL[n.categoria])} — ${escapeHtml(n.titulo)}</div>
                    <div class="notif-desc">${escapeHtml(n.descricao)}</div>
                    <div class="notif-meta">👤 ${escapeHtml(n.responsavel)} &nbsp;·&nbsp; 📅 ${escapeHtml(n.vencimento)}</div>
                </div>
            </div>
        `).join('');

        // Event delegation em vez de listener por item (previne memory leak)
        list.onclick = function(e) {
            const item = e.target.closest('.notif-item');
            if (!item) return;
            const id = parseInt(item.dataset.id);
            const notif = NOTIFICATIONS.find(n => n.id === id);
            if (notif) { notif.lida = true; renderNotifications(); }
        };
    }

    // Filter buttons
    document.querySelectorAll('.notif-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.notif-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderNotifications();
        });
    });

    document.getElementById('markAllRead').addEventListener('click', () => {
        NOTIFICATIONS.forEach(n => n.lida = true);
        renderNotifications();
    });

    // Open / Close notification panel
    document.getElementById('notifBtn').addEventListener('click', (e) => {
        e.stopPropagation();
        closeUserDropdown();
        document.getElementById('notifPanel').classList.toggle('open');
        document.getElementById('notifOverlay').classList.toggle('open');
    });

    document.getElementById('notifClose').addEventListener('click', closeNotifPanel);
    document.getElementById('notifOverlay').addEventListener('click', closeNotifPanel);

    function closeNotifPanel() {
        document.getElementById('notifPanel').classList.remove('open');
        document.getElementById('notifOverlay').classList.remove('open');
    }

    // ============================================================
    // AUTH STATE (simulated — replace with real AuthContext/API)
    // ============================================================
    const AuthState = {
        user: {
            name: 'Guilherme Ferreira',
            initials: 'GF',
            role: 'Acad. Enfermagem',
            email: 'guilherme.ferreira@ucgs.edu.br',
            sector: 'Enfermagem — Ambulatório',
            registrationId: 'UCGS-2024-0847',
            avatarUrl: null // null = fallback to initials
        },
        isAuthenticated: true,
        clear() {
            this.user = null;
            this.isAuthenticated = false;
            localStorage.removeItem('ucgs_auth_token');
            localStorage.removeItem('ucgs_user_data');
            sessionStorage.clear();
        }
    };

    // Hydrate UI from auth state
    function hydrateUserUI() {
        const u = AuthState.user;
        if (!u) return;
        const setText = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
        setText('dropdownUserName', u.name);
        setText('dropdownUserRole', u.role);
        setText('profileName', u.name);
        setText('profileRole', u.role);
        setText('profileEmail', u.email);
        setText('profileSector', u.sector);
        setText('profileId', u.registrationId);

        // Avatar (header + profile modal)
        const headerAvatar = document.getElementById('userMenuBtn');
        const profileAvatar = document.getElementById('profileAvatar');
        if (u.avatarUrl) {
            headerAvatar.innerHTML = '<img src="' + u.avatarUrl + '" alt="' + u.name + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">';
            profileAvatar.innerHTML = '<img src="' + u.avatarUrl + '" alt="' + u.name + '">';
        } else {
            headerAvatar.textContent = u.initials;
            profileAvatar.textContent = u.initials;
        }
    }
    hydrateUserUI();

    // ============================================================
    // USER DROPDOWN
    // ============================================================
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    const menuItems = userDropdown.querySelectorAll('.dropdown-item');

    function openUserDropdown() {
        closeNotifPanel();
        userDropdown.classList.add('open');
        userMenuBtn.setAttribute('aria-expanded', 'true');
        if (menuItems.length) menuItems[0].focus();
    }

    function closeUserDropdown() {
        userDropdown.classList.remove('open');
        userMenuBtn.setAttribute('aria-expanded', 'false');
    }

    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.contains('open') ? closeUserDropdown() : openUserDropdown();
    });

    userMenuBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
            e.preventDefault();
            openUserDropdown();
        }
    });

    // Keyboard navigation inside dropdown
    userDropdown.addEventListener('keydown', (e) => {
        const items = Array.from(menuItems);
        const current = document.activeElement;
        const idx = items.indexOf(current);

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const next = idx < items.length - 1 ? idx + 1 : 0;
            items[next].focus();
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prev = idx > 0 ? idx - 1 : items.length - 1;
            items[prev].focus();
        } else if (e.key === 'Escape') {
            e.preventDefault();
            closeUserDropdown();
            userMenuBtn.focus();
        } else if (e.key === 'Tab') {
            closeUserDropdown();
        }
    });

    document.addEventListener('click', () => closeUserDropdown());
    userDropdown.addEventListener('click', e => e.stopPropagation());

    // ============================================================
    // PROFILE MODAL
    // ============================================================
    const profileOverlay = document.getElementById('profileOverlay');
    const profileClose = document.getElementById('profileClose');

    function openProfileModal() {
        hydrateUserUI();
        profileOverlay.classList.add('open');
        document.body.style.overflow = 'hidden';
        profileClose.focus();
    }

    function closeProfileModal() {
        profileOverlay.classList.remove('open');
        document.body.style.overflow = '';
        userMenuBtn.focus();
    }

    document.getElementById('viewProfileBtn').addEventListener('click', () => {
        closeUserDropdown();
        openProfileModal();
    });

    profileClose.addEventListener('click', closeProfileModal);

    profileOverlay.addEventListener('click', (e) => {
        if (e.target === profileOverlay) closeProfileModal();
    });

    profileOverlay.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeProfileModal();
        // Trap focus inside modal
        if (e.key === 'Tab') {
            const focusable = profileOverlay.querySelectorAll('button, [tabindex]:not([tabindex="-1"])');
            if (focusable.length === 0) return;
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });

    // ============================================================
    // LOGOUT
    // ============================================================
    document.getElementById('logoutBtn').addEventListener('click', () => {
        closeUserDropdown();

        const confirmed = confirm('Deseja realmente sair do sistema?');
        if (!confirmed) return;

        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.classList.add('logout-loading');

        // Simulate async logout (replace with real API call)
        setTimeout(() => {
            try {
                // Clear all auth data
                AuthState.clear();

                // Clear any remaining storage
                localStorage.removeItem('sst_theme');
                document.cookie.split(';').forEach(c => {
                    document.cookie = c.trim().split('=')[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
                });

                // In production: window.location.href = '/login';
                logoutBtn.classList.remove('logout-loading');
                document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:Inter,sans-serif;background:#F8FAFC;"><div style="text-align:center;"><div style="font-size:2rem;margin-bottom:16px;">👋</div><h2 style="color:#0F172A;margin-bottom:8px;">Sessão encerrada</h2><p style="color:#64748B;margin-bottom:24px;">Você foi desconectado com segurança.</p><button onclick="location.reload()" style="padding:10px 24px;background:#0EA5E9;color:white;border:none;border-radius:8px;font-size:0.875rem;font-weight:600;cursor:pointer;">Fazer login novamente</button></div></div>';
            } catch (err) {
                logoutBtn.classList.remove('logout-loading');
                alert('Erro ao encerrar sessão. Tente novamente.');
            }
        }, 600);
    });

    // ============================================================
    // DARK MODE — persiste no localStorage
    // ============================================================
    const themeToggle = document.getElementById('themeToggle');

    function applyTheme(dark) {
        document.body.classList.toggle('dark-mode', dark);
        themeToggle.checked = dark;
        localStorage.setItem('sst_theme', dark ? 'dark' : 'light');
    }

    // Load saved preference
    const savedTheme = localStorage.getItem('sst_theme');
    applyTheme(savedTheme === 'dark');

    themeToggle.addEventListener('change', () => applyTheme(themeToggle.checked));

    // ============================================================
    // SEARCH ENGINE — Typeahead / Autocomplete com Debounce
    // Simula endpoint GET /api/search?q=<query>
    // Estrutura de resposta: { title, category, url, icon }
    // ============================================================

    /**
     * BASE DE DADOS DE RECURSOS DO SISTEMA
     * Em produção: substituir por chamada fetch() ao endpoint REST.
     * Cada item representa um recurso navegável do sistema.
     */
    const SEARCH_INDEX = [
        // ── Páginas ──────────────────────────────────────────────
        { title: 'Painel de Controle',        category: 'Página',    icon: '📊', section: 'dashboard',       desc: 'Visão geral e alertas prioritários' },
        { title: 'Mapas de Risco',             category: 'Página',    icon: '🗺️', section: 'mapas-risco',     desc: 'Gestão de mapas de risco por setor' },
        { title: 'Protocolos de Segurança',    category: 'Página',    icon: '📋', section: 'protocolos',      desc: 'Biblioteca de protocolos SST' },
        { title: 'Controle de Vacinação',      category: 'Página',    icon: '💉', section: 'vacinacao',       desc: 'Cartões e campanhas de vacinação' },
        { title: 'Análises e Métricas',        category: 'Página',    icon: '📈', section: 'analises',        desc: 'Gráficos de desempenho e tendências' },
        { title: 'Histórico de Eventos',       category: 'Página',    icon: '📋', section: 'historico',       desc: 'Registro histórico de incidentes' },
        { title: 'Configurações',              category: 'Página',    icon: '⚙️', section: 'configuracoes',   desc: 'Preferências e parametrizações' },
        { title: 'Contatos',                   category: 'Página',    icon: '📞', section: 'contatos',         desc: 'Vigilância Sanitária e Epidemiológica de Alfenas' },
        { title: 'Psicologia Clínica',         category: 'Página',    icon: '🧠', section: 'psicologia',      desc: 'Atendimento psicológico, prontuário e evolução clínica' },
        { title: 'Exames Clínicos',            category: 'Página',    icon: '🔬', section: 'exames',          desc: 'Laboratoriais, imagem, evolução temporal e interpretação clínica' },

        // ── Exames ──────────────────────────────────────────────
        { title: 'Hemograma Completo',          category: 'Exame', icon: '🩸', section: 'exames', desc: 'Eritrócitos, leucócitos, plaquetas — laboratorial' },
        { title: 'Glicemia de Jejum',           category: 'Exame', icon: '⚗️', section: 'exames', desc: 'Bioquímica — valor de referência: 70–99 mg/dL' },
        { title: 'Creatinina Sérica',           category: 'Exame', icon: '⚗️', section: 'exames', desc: 'Função renal — bioquímica' },
        { title: 'TSH',                         category: 'Exame', icon: '🧬', section: 'exames', desc: 'Hormônio tireoestimulante — hormonal' },
        { title: 'Raio-X Tórax',               category: 'Exame', icon: '📷', section: 'exames', desc: 'Exame de imagem — tórax PA e perfil' },
        { title: 'Urocultura',                  category: 'Exame', icon: '🦠', section: 'exames', desc: 'Microbiologia — cultura de urina' },

        // ── Psicologia ───────────────────────────────────────────
        { title: 'Anamnese Psicológica',       category: 'Psicologia', icon: '🧠', section: 'psicologia', desc: 'Coleta inicial, exame do estado mental, avaliação de risco' },
        { title: 'Evolução Clínica – Psicologia', category: 'Psicologia', icon: '🧠', section: 'psicologia', desc: 'Registro de sessões, intervenções e observações' },
        { title: 'Diagnóstico DSM-5 / CID-10', category: 'Psicologia', icon: '🧠', section: 'psicologia', desc: 'Hipótese diagnóstica e histórico diagnóstico' },
        { title: 'Plano Terapêutico',          category: 'Psicologia', icon: '🧠', section: 'psicologia', desc: 'Objetivos SMART, abordagem e critérios de alta' },
        { title: 'Maria Silva Santos – PSI-2024-0847', category: 'Psicologia', icon: '🧠', section: 'psicologia', desc: 'Depressão moderada · Ansiedade generalizada · Risco moderado' },

        // ── Contatos ─────────────────────────────────────────────
        { title: 'Vigilância Sanitária de Alfenas',      category: 'Contato', icon: '🏥', section: 'contatos', desc: 'Tel: (35) 3698-1789 · Parque das Nações, Alfenas – MG' },
        { title: 'Vigilância Epidemiológica de Alfenas', category: 'Contato', icon: '🔬', section: 'contatos', desc: 'Tel: (35) 3698-2154 · Vila Formosa, Alfenas – MG' },

        // ── Mapas de Risco ────────────────────────────────────────
        { title: 'Setor A – Enfermaria',       category: 'Mapa de Risco', icon: '🗺️', section: 'mapas-risco', desc: 'Risco biológico · Alto · Em dia' },
        { title: 'Setor B – Oficina Mecânica', category: 'Mapa de Risco', icon: '🗺️', section: 'mapas-risco', desc: 'Risco físico · Crítico · Vencido ⚠️' },
        { title: 'Setor C – Lavanderia',       category: 'Mapa de Risco', icon: '🗺️', section: 'mapas-risco', desc: 'Risco químico · Alto · Em dia' },
        { title: 'Setor D – Cozinha',          category: 'Mapa de Risco', icon: '🗺️', section: 'mapas-risco', desc: 'Risco ergonômico · Médio · Em dia' },

        // ── Protocolos ────────────────────────────────────────────
        { title: 'Protocolo de Perfurocortantes',    category: 'Protocolo', icon: '📋', section: 'protocolos', desc: 'NR-32 · Revisão vencida em 15/03/2026' },
        { title: 'Protocolo de Riscos Químicos',     category: 'Protocolo', icon: '📋', section: 'protocolos', desc: 'NR-09 · Pendente de atualização' },
        { title: 'Protocolo de Ergonomia',           category: 'Protocolo', icon: '📋', section: 'protocolos', desc: 'NR-17 · Válido até 10/08/2026' },
        { title: 'Protocolo de Incêndio e Pânico',   category: 'Protocolo', icon: '📋', section: 'protocolos', desc: 'NR-23 · Válido até 01/06/2026' },
        { title: 'Protocolo de EPI Obrigatório',     category: 'Protocolo', icon: '📋', section: 'protocolos', desc: 'NR-06 · Atualizado em 20/01/2026' },

        // ── Vacinação ─────────────────────────────────────────────
        { title: 'Vacinação – Detento #235',         category: 'Vacina', icon: '💉', section: 'vacinacao', desc: 'Hepatite B + Tétano pendentes' },
        { title: 'Campanha Influenza 2026',           category: 'Vacina', icon: '💉', section: 'vacinacao', desc: 'Prevista para 05/04/2026' },
        { title: 'Campanha Hepatite B',               category: 'Vacina', icon: '💉', section: 'vacinacao', desc: 'Em andamento · 82% concluída' },

        // ── Relatórios ────────────────────────────────────────────
        { title: 'Relatório de Acidentes – Mar/2026', category: 'Relatório', icon: '📄', section: 'analises', desc: '4 ocorrências · -25% vs mês anterior' },
        { title: 'Relatório de Conformidade NR-32',   category: 'Relatório', icon: '📄', section: 'analises', desc: 'Gerado em 01/03/2026' },
        { title: 'Relatório de Vacinação – Mar/2026', category: 'Relatório', icon: '📄', section: 'analises', desc: '89% em dia · 234 de 263 pessoas' },

        // ── Usuários/Responsáveis ─────────────────────────────────
        { title: 'Dra. Maria Costa',      category: 'Responsável', icon: '👤', section: 'configuracoes', desc: 'Médica do Trabalho · Protocolos NR-32' },
        { title: 'Eng. Carlos Alves',     category: 'Responsável', icon: '👤', section: 'configuracoes', desc: 'Engenheiro de Segurança · Riscos Químicos' },
        { title: 'Enf. Pedro Santos',     category: 'Responsável', icon: '👤', section: 'configuracoes', desc: 'Enfermeiro · Controle de Vacinação' },
        { title: 'João Silva',            category: 'Responsável', icon: '👤', section: 'configuracoes', desc: 'Técnico de Segurança · Mapa de Risco Setor B' },
    ];

    /**
     * CATEGORIA DISPLAY CONFIG
     * Define label e cor do badge para cada categoria.
     */
    const CATEGORY_CONFIG = {
        'Página':        { label: 'Páginas',       color: '#0EA5E9' },
        'Mapa de Risco': { label: 'Mapas de Risco', color: '#8B5CF6' },
        'Protocolo':     { label: 'Protocolos',    color: '#F97316' },
        'Vacina':        { label: 'Vacinas',        color: '#10B981' },
        'Exame':         { label: 'Exames',         color: '#3B82F6' },
        'Relatório':     { label: 'Relatórios',    color: '#64748B' },
        'Responsável':   { label: 'Responsáveis',  color: '#6366F1' },
        'Psicologia':    { label: 'Psicologia',     color: '#4A7C8E' },
        'Contato':       { label: 'Contatos',       color: '#0EA5E9' },
    };

    /**
     * Mock de endpoint: GET /api/search?q=<query>
     * Simula latência de rede (50ms) e retorna resultados ranqueados.
     * Em produção: substituir por fetch('/api/search?q=' + encodeURIComponent(query))
     *
     * @param {string} query — string de busca
     * @returns {Promise<Array>} — array de { title, category, url, icon, desc }
     */
    function mockSearchAPI(query) {
        return new Promise(resolve => {
            setTimeout(() => {
                const q = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
                const results = SEARCH_INDEX
                    .filter(item => {
                        const haystack = (item.title + ' ' + item.desc + ' ' + item.category)
                            .toLowerCase()
                            .normalize('NFD')
                            .replace(/[\u0300-\u036f]/g, '');
                        return haystack.includes(q);
                    })
                    .map(item => ({
                        title:    item.title,
                        category: item.category,
                        url:      '#section/' + item.section,
                        icon:     item.icon,
                        desc:     item.desc,
                        section:  item.section,
                    }));
                resolve(results);
            }, 50);
        });
    }

    /**
     * Utilitário: destaca o trecho matched na string.
     * @param {string} text — texto original
     * @param {string} query — busca do usuário
     * @returns {string} — HTML com <mark> nos trechos correspondentes
     */
    function highlight(text, query) {
        if (!query) return escapeHtml(text);
        const safeText = escapeHtml(text);
        const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const re = new RegExp(`(${escapeHtml(escaped)})`, 'gi');
        return safeText.replace(re, '<mark>$1</mark>');
    }

    /**
     * Renderiza os resultados agrupados por categoria no dropdown.
     * @param {Array} results
     * @param {string} query
     */
    function renderSearchResults(results, query) {
        const dropdown = document.getElementById('searchDropdown');

        if (results.length === 0) {
            dropdown.innerHTML = `
                <div class="search-empty">
                    <div class="search-empty-icon">🔎</div>
                    <div class="search-empty-title">Nenhum resultado encontrado</div>
                    <div class="search-empty-sub">Tente outro termo ou verifique a ortografia.</div>
                </div>`;
            dropdown.classList.add('open');
            return;
        }

        // Agrupar por categoria preservando a ordem de CATEGORY_CONFIG
        const groups = {};
        results.forEach(item => {
            if (!groups[item.category]) groups[item.category] = [];
            groups[item.category].push(item);
        });

        let html = '';
        Object.entries(groups).forEach(([category, items]) => {
            const cfg = CATEGORY_CONFIG[category] || { label: category };
            html += `<div class="search-category-label">${escapeHtml(cfg.label)}</div>`;
            items.forEach((item, idx) => {
                const titleHL = highlight(item.title, query);
                html += `
                    <div class="search-result-item" role="option" tabindex="-1"
                         data-section="${escapeHtml(item.section)}" data-idx="${idx}">
                        <div class="search-result-icon">${escapeHtml(item.icon)}</div>
                        <div class="search-result-info">
                            <div class="search-result-title">${titleHL}</div>
                            <div class="search-result-sub">${escapeHtml(item.desc)}</div>
                        </div>
                        <span class="search-result-badge">${escapeHtml(cfg.label)}</span>
                    </div>`;
            });
        });

        html += `
            <div class="search-footer">
                <span class="search-footer-hint">
                    <span class="search-kbd">↑↓</span> navegar &nbsp;
                    <span class="search-kbd">↵</span> selecionar &nbsp;
                    <span class="search-kbd">Esc</span> fechar
                </span>
                <span class="search-footer-hint">${results.length} resultado${results.length !== 1 ? 's' : ''}</span>
            </div>`;

        dropdown.innerHTML = html;
        dropdown.classList.add('open');

        // Event delegation — um único listener no dropdown (previne memory leak)
        dropdown.onmousedown = function(e) {
            const el = e.target.closest('.search-result-item');
            if (!el) return;
            e.preventDefault(); // evita blur no input antes do click
            navigateToSection(el.dataset.section);
            closeSearchDropdown();
        };
    }

    /**
     * Navega para a seção do dashboard e atualiza a sidebar.
     * Compatível com rotas internas por âncora (#section/<id>).
     * @param {string} sectionId
     */
    function navigateToSection(sectionId) {
        // Ativa seção de conteúdo
        document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
        const target = document.getElementById(sectionId);
        if (target) {
            target.classList.add('active');
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Sincroniza sidebar nav
        document.querySelectorAll('.nav-item').forEach(nav => {
            nav.classList.toggle('active', nav.dataset.section === sectionId);
        });

        // Atualiza hash para suporte a deep-link (sem scroll automático do browser)
        history.replaceState(null, '', '#section/' + sectionId);

        // Limpa o input após navegação
        const input = document.getElementById('searchInput');
        input.value = '';
        document.getElementById('searchBar').classList.remove('has-value', 'focused');
    }

    /**
     * Fecha e limpa o dropdown.
     */
    function closeSearchDropdown() {
        const dropdown = document.getElementById('searchDropdown');
        dropdown.classList.remove('open');
        dropdown.innerHTML = '';
        activeResultIndex = -1;
    }

    // ── Debounce ──────────────────────────────────────────────────
    let _searchTimer = null;
    let activeResultIndex = -1;

    /**
     * Debounce: aguarda 280ms após última tecla antes de consultar a API.
     * Evita chamadas excessivas e melhora performance percebida.
     */
    function debounceSearch(query) {
        clearTimeout(_searchTimer);
        const searchBar = document.getElementById('searchBar');
        if (!query.trim()) {
            searchBar.classList.remove('loading');
            closeSearchDropdown();
            return;
        }
        searchBar.classList.add('loading');
        _searchTimer = setTimeout(async () => {
            const results = await mockSearchAPI(query.trim());
            searchBar.classList.remove('loading');
            renderSearchResults(results, query.trim());
        }, 320);
    }

    // ── Keyboard Navigation ───────────────────────────────────────
    function getResultItems() {
        return document.querySelectorAll('#searchDropdown .search-result-item');
    }

    function setActiveResult(index) {
        const items = getResultItems();
        items.forEach(i => i.classList.remove('active'));
        activeResultIndex = Math.max(-1, Math.min(index, items.length - 1));
        if (activeResultIndex >= 0) {
            items[activeResultIndex].classList.add('active');
            items[activeResultIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    // ── Event Listeners ───────────────────────────────────────────
    const searchInput = document.getElementById('searchInput');
    const searchBar   = document.getElementById('searchBar');
    const searchClear = document.getElementById('searchClear');

    searchInput.addEventListener('input', e => {
        const val = e.target.value;
        searchBar.classList.toggle('has-value', val.length > 0);
        activeResultIndex = -1;
        debounceSearch(val);
    });

    searchInput.addEventListener('focus', () => {
        searchBar.classList.add('focused');
        if (searchInput.value.trim()) {
            debounceSearch(searchInput.value.trim());
        }
    });

    searchInput.addEventListener('blur', () => {
        searchBar.classList.remove('focused');
        // Delay para permitir o click no item antes de fechar
        setTimeout(closeSearchDropdown, 150);
    });

    searchInput.addEventListener('keydown', e => {
        const dropdown = document.getElementById('searchDropdown');
        if (!dropdown.classList.contains('open')) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActiveResult(activeResultIndex + 1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActiveResult(activeResultIndex - 1);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            const items = getResultItems();
            if (activeResultIndex >= 0 && items[activeResultIndex]) {
                navigateToSection(items[activeResultIndex].dataset.section);
                closeSearchDropdown();
                searchInput.blur();
            }
        } else if (e.key === 'Escape') {
            closeSearchDropdown();
            searchInput.blur();
        }
    });

    // Atalho global: '/' abre a busca (padrão em dashboards profissionais)
    document.addEventListener('keydown', e => {
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    });

    searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchBar.classList.remove('has-value');
        closeSearchDropdown();
        searchInput.focus();
    });

    // Fecha ao clicar fora
    document.addEventListener('click', e => {
        if (!searchBar.contains(e.target)) closeSearchDropdown();
    });

    // ============================================================
    // ANÁLISES E MÉTRICAS — Dashboard Completo v2
    // Motor de dados, filtros, drill-down, exportação, insights
    // ============================================================
    (function () {
        'use strict';

        /* ══════════════════════════════════════════════════════════
           DATA LAYER — mock realista com variação por período
           ══════════════════════════════════════════════════════════ */
        const AGENT_COLORS = { 'Ácidos':'#F43F5E','Solventes':'#F97316','Cáusticos':'#F59E0B','Oxidantes':'#14B8A6','Outros':'#8B5CF6' };

        const MOCK_DB = {
            '7d': {
                labels:['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                perf:[2,1,3,0,2,1,0], notif:[2,1,2,0,2,1,0],
                fis:[1,0,2,1,0,0,0], quim:[0,2,1,0,1,0,1],
                kpis:{ total:14, perf:9, delta:-8, days:14, record:31, bio:3,
                       vaccPct:89, vaccUp:234, vaccPend:19, vaccOver:10, vaccTotal:263 },
                donut:{labels:['Ácidos','Solventes','Cáusticos','Oxidantes','Outros'],values:[3,2,1,1,2]},
                setor:{labels:['Enfermaria A','Enfermaria B','Farmácia','Laboratório','Triagem','Almoxarifado'],values:[4,5,2,3,1,0]},
                sparks:{ bioExp:[1,0,1,0,1,0,0], daysNo:[8,9,10,11,12,13,14] },
            },
            '30d': {
                labels:['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12'],
                perf:[5,3,6,4,2,5,3,4,2,6,3,5], notif:[4,3,5,4,2,4,2,3,2,5,3,4],
                fis:[3,2,4,3,1,3,2,2,1,4,2,3], quim:[4,5,3,6,2,4,5,3,2,5,4,6],
                kpis:{ total:47, perf:18, delta:-12, days:14, record:31, bio:8,
                       vaccPct:89, vaccUp:234, vaccPend:19, vaccOver:10, vaccTotal:263 },
                donut:{labels:['Ácidos','Solventes','Cáusticos','Oxidantes','Outros'],values:[28,22,18,14,18]},
                setor:{labels:['Enfermaria A','Enfermaria B','Farmácia','Laboratório','Triagem','Almoxarifado'],values:[38,44,22,31,17,12]},
                sparks:{ bioExp:[2,1,2,1,0,1,0,1,0,1,0,0], daysNo:[0,3,5,0,2,7,10,0,4,8,12,14] },
            },
            '90d': {
                labels:['JW1','JW2','JW3','JW4','FW1','FW2','FW3','FW4','MW1','MW2','MW3','MW4'],
                perf:[8,6,9,7,5,7,6,5,4,6,5,3], notif:[7,5,8,6,5,6,5,4,4,5,4,3],
                fis:[5,4,6,5,3,4,4,3,2,3,3,2], quim:[6,8,5,9,4,6,7,5,3,5,6,4],
                kpis:{ total:127, perf:48, delta:-18, days:14, record:31, bio:19,
                       vaccPct:89, vaccUp:234, vaccPend:19, vaccOver:10, vaccTotal:263 },
                donut:{labels:['Ácidos','Solventes','Cáusticos','Oxidantes','Outros'],values:[22,18,15,11,14]},
                setor:{labels:['Enfermaria A','Enfermaria B','Farmácia','Laboratório','Triagem','Almoxarifado'],values:[32,38,18,26,14,10]},
                sparks:{ bioExp:[3,2,3,2,1,2,1,2,1,1,0,1], daysNo:[0,5,0,3,8,0,4,9,0,6,12,14] },
            },
            '12m': {
                labels:['Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar'],
                perf:[12,10,14,11,9,13,10,8,11,9,7,5], notif:[10,9,12,10,8,11,9,7,10,8,6,4],
                fis:[8,7,9,7,6,8,6,5,7,5,4,3], quim:[10,12,8,11,7,9,10,8,9,8,7,5],
                kpis:{ total:243, perf:94, delta:-22, days:14, record:31, bio:37,
                       vaccPct:89, vaccUp:234, vaccPend:19, vaccOver:10, vaccTotal:263 },
                donut:{labels:['Ácidos','Solventes','Cáusticos','Oxidantes','Outros'],values:[28,22,18,14,18]},
                setor:{labels:['Enfermaria A','Enfermaria B','Farmácia','Laboratório','Triagem','Almoxarifado'],values:[38,44,22,31,17,12]},
                sparks:{ bioExp:[5,4,5,3,3,4,3,2,3,2,1,2], daysNo:[0,3,0,5,0,2,8,0,4,10,0,14] },
            },
        };

        /* Setor filter multipliers (simulate filtering) */
        const SETOR_MULT = { all:1, enfermaria_a:0.23, enfermaria_b:0.27, farmacia:0.13, laboratorio:0.19, triagem:0.10, almoxarifado:0.08 };
        const TIPO_MULT  = { all:1, perfurocortante:0.38, fisico:0.28, quimico:0.24, biologico:0.10 };

        /* ── Estado ─────────────────────────────────────────────── */
        let amPeriod = '30d';
        let amFilterSetor = 'all';
        let amFilterTipo = 'all';
        let amChartPerf, amChartFQ, amChartDonut, amChartSetor;
        let amDdChartInst = null;
        const amSparks = {};
        let amInitialized = false;
        let amCurrentData = null;

        /* ── Helpers ────────────────────────────────────────────── */
        function amRgba(hex, a) {
            const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
            return `rgba(${r},${g},${b},${a})`;
        }
        function amTrend(data) {
            const n = data.length, xs = [...Array(n).keys()];
            const mx = xs.reduce((a,x)=>a+x,0)/n, my = data.reduce((a,y)=>a+y,0)/n;
            const num = xs.reduce((a,x,i)=>a+(x-mx)*(data[i]-my),0);
            const den = xs.reduce((a,x)=>a+(x-mx)**2,0)||1;
            const m = num/den, b = my-m*mx;
            return xs.map(x=>+(m*x+b).toFixed(2));
        }
        function amSum(arr) { return arr.reduce((a,b)=>a+b,0); }
        function amApplyMult(arr, mult) { return arr.map(v => Math.round(v * mult)); }
        function amEl(id) { return document.getElementById(id); }

        /* ── Toast ──────────────────────────────────────────────── */
        function amToast(msg, type) {
            const el = amEl('amToast');
            if (!el) return;
            el.className = 'am-toast am-toast-' + (type || 'info');
            el.textContent = msg;
            requestAnimationFrame(() => { el.classList.add('show'); });
            setTimeout(() => { el.classList.remove('show'); }, 3200);
        }

        /* ── Loading overlay ────────────────────────────────────── */
        function amSetLoading(on) {
            const el = amEl('amLoadingOverlay');
            if (el) el.style.display = on ? 'flex' : 'none';
        }

        /* ── Tooltip config (shared) ────────────────────────────── */
        const amTooltipCfg = {
            backgroundColor:'#fff', titleColor:'#0F172A', bodyColor:'#64748B',
            borderColor:'#E2E8F0', borderWidth:1, padding:12, cornerRadius:10,
            titleFont:{weight:'700',size:12}, bodyFont:{size:11},
            displayColors:true, boxPadding:4,
        };

        /* ══════════════════════════════════════════════════════════
           GET FILTERED DATA — applies sector+type multipliers
           ══════════════════════════════════════════════════════════ */
        function amGetData(period) {
            const raw = MOCK_DB[period];
            const sm = SETOR_MULT[amFilterSetor];
            const tm = TIPO_MULT[amFilterTipo];
            const m = sm * tm / (sm === 1 && tm === 1 ? 1 : 0.38); // normalize
            const mult = sm === 1 && tm === 1 ? 1 : Math.max(0.15, Math.min(m, 1.2));

            return {
                labels: raw.labels,
                perf: amApplyMult(raw.perf, mult),
                notif: amApplyMult(raw.notif, mult),
                fis: amApplyMult(raw.fis, mult),
                quim: amApplyMult(raw.quim, mult),
                kpis: {
                    total: Math.round(raw.kpis.total * mult),
                    perf: Math.round(raw.kpis.perf * mult),
                    delta: raw.kpis.delta,
                    days: raw.kpis.days,
                    record: raw.kpis.record,
                    bio: Math.round(raw.kpis.bio * mult),
                    vaccPct: raw.kpis.vaccPct,
                    vaccUp: raw.kpis.vaccUp,
                    vaccPend: raw.kpis.vaccPend,
                    vaccOver: raw.kpis.vaccOver,
                    vaccTotal: raw.kpis.vaccTotal,
                },
                donut: { labels: raw.donut.labels, values: amApplyMult(raw.donut.values, mult) },
                setor: { labels: raw.setor.labels, values: amApplyMult(raw.setor.values, mult) },
                sparks: {
                    bioExp: amApplyMult(raw.sparks.bioExp, mult),
                    daysNo: raw.sparks.daysNo,
                },
            };
        }

        /* ══════════════════════════════════════════════════════════
           CHARTS — build functions
           ══════════════════════════════════════════════════════════ */
        function amBuildPerf(d) {
            const el = amEl('amChartPerf'); if (!el) return;
            const c = el.getContext('2d');
            const gO = c.createLinearGradient(0,0,0,220);
            gO.addColorStop(0,'rgba(244,63,94,0.28)'); gO.addColorStop(1,'rgba(244,63,94,0)');
            const gN = c.createLinearGradient(0,0,0,220);
            gN.addColorStop(0,'rgba(14,165,233,0.18)'); gN.addColorStop(1,'rgba(14,165,233,0)');
            if (amChartPerf) amChartPerf.destroy();
            amChartPerf = new Chart(el, {
                type:'line',
                data:{ labels:d.labels, datasets:[
                    { label:'Ocorrências', data:d.perf, borderColor:'#F43F5E', backgroundColor:gO, borderWidth:2.5, fill:true, tension:0.45, pointRadius:4, pointHoverRadius:7, pointBackgroundColor:'#F43F5E', pointBorderColor:'#fff', pointBorderWidth:2 },
                    { label:'Notificados', data:d.notif, borderColor:'#0EA5E9', backgroundColor:gN, borderWidth:2, fill:true, tension:0.45, pointRadius:3, pointHoverRadius:6, pointBackgroundColor:'#0EA5E9', pointBorderColor:'#fff', pointBorderWidth:2 },
                    { label:'Tendência', data:amTrend(d.perf), borderColor:'#8B5CF6', borderDash:[5,4], borderWidth:1.5, fill:false, tension:0, pointRadius:0 },
                ]},
                options:{ responsive:true, maintainAspectRatio:false, interaction:{mode:'index',intersect:false}, animation:{duration:900,easing:'easeOutQuart'},
                    onClick:(evt,elems)=>{ if(elems.length){ const idx=elems[0].index; amDrilldownPoint('perf',idx); } },
                    plugins:{ legend:{display:false}, tooltip:amTooltipCfg },
                    scales:{ x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{color:'#94A3B8',font:{size:10}}}, y:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{color:'#94A3B8',font:{size:10}},beginAtZero:true} },
                },
            });
        }

        function amBuildFQ(d) {
            const el = amEl('amChartFisQuim'); if (!el) return;
            const c = el.getContext('2d');
            const gF = c.createLinearGradient(0,0,0,220); gF.addColorStop(0,'#FB923C'); gF.addColorStop(1,'#F97316');
            const gQ = c.createLinearGradient(0,0,0,220); gQ.addColorStop(0,'#2DD4BF'); gQ.addColorStop(1,'#14B8A6');
            if (amChartFQ) amChartFQ.destroy();
            amChartFQ = new Chart(el, {
                type:'bar',
                data:{ labels:d.labels, datasets:[
                    { label:'Físicos', data:d.fis, backgroundColor:gF, borderColor:'#EA580C', borderWidth:1, borderRadius:5, borderSkipped:false, hoverBackgroundColor:'#FDBA74' },
                    { label:'Químicos', data:d.quim, backgroundColor:gQ, borderColor:'#0D9488', borderWidth:1, borderRadius:5, borderSkipped:false, hoverBackgroundColor:'#5EEAD4' },
                ]},
                options:{ responsive:true, maintainAspectRatio:false, interaction:{mode:'index',intersect:false},
                    animation:{ duration:900, easing:'easeOutBounce', delay:ctx=>ctx.dataIndex*25 },
                    onClick:(evt,elems)=>{ if(elems.length){ const idx=elems[0].index; amDrilldownPoint('fq',idx); } },
                    plugins:{ legend:{display:false}, tooltip:amTooltipCfg },
                    scales:{ x:{grid:{display:false},ticks:{color:'#94A3B8',font:{size:10},maxRotation:45}}, y:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{color:'#94A3B8',font:{size:10}},beginAtZero:true} },
                },
            });
        }

        function amAnimateGauge(pct) {
            const tot = 251.2, fill = tot * (1 - pct / 100);
            const path = amEl('amGaugeFill');
            const needle = amEl('amGaugeNeedle');
            const txt = amEl('amGaugeValTxt');
            if (path) {
                path.style.transition = 'none';
                path.style.strokeDashoffset = tot;
                path.getBoundingClientRect();
                path.style.transition = 'stroke-dashoffset 1.6s cubic-bezier(0.34,1.56,0.64,1)';
                path.style.strokeDashoffset = fill;
            }
            if (needle) needle.style.transform = `rotate(${-90 + (pct / 100) * 180}deg)`;
            if (txt) {
                let t0 = null;
                const dur = 1400;
                requestAnimationFrame(function run(ts) {
                    if (!t0) t0 = ts;
                    const p = Math.min((ts - t0) / dur, 1);
                    const ease = p < 0.5 ? 2*p*p : 1 - Math.pow(-2*p+2,2)/2;
                    txt.textContent = Math.round(ease * pct) + '%';
                    if (p < 1) requestAnimationFrame(run);
                });
            }
        }

        function amBuildDonut(donut) {
            const el = amEl('amChartDonut'); if (!el) return;
            const colors = donut.labels.map(l => AGENT_COLORS[l] ?? '#8B5CF6');
            if (amChartDonut) amChartDonut.destroy();
            amChartDonut = new Chart(el, {
                type:'doughnut',
                data:{ labels:donut.labels, datasets:[{ data:donut.values, backgroundColor:colors, hoverBackgroundColor:colors.map(c=>c+'CC'), borderColor:'#fff', borderWidth:3, hoverOffset:10, borderRadius:4 }]},
                options:{ responsive:true, maintainAspectRatio:false, cutout:'68%', animation:{animateRotate:true,animateScale:true,duration:1000,easing:'easeOutQuart'},
                    onClick:(evt,elems)=>{ if(elems.length){ amDrilldownDonutSlice(elems[0].index); } },
                    plugins:{ legend:{display:false}, tooltip:{...amTooltipCfg, callbacks:{ label:ctx=>{ const t=ctx.dataset.data.reduce((a,b)=>a+b,0); return ` ${ctx.label}: ${ctx.parsed} (${((ctx.parsed/t)*100).toFixed(1)}%)`; }}} },
                },
            });
            const tot = amSum(donut.values) || 1;
            const lg = amEl('amDonutLegend');
            if (lg) lg.innerHTML = donut.labels.map((l,i) =>
                `<div class="am-donut-legend-item"><div class="am-donut-legend-dot" style="background:${colors[i]};"></div><span class="am-donut-legend-lbl">${l}</span><span class="am-donut-legend-pct">${((donut.values[i]/tot)*100).toFixed(0)}%</span></div>`
            ).join('');
        }

        function amBuildSetor(setor) {
            const el = amEl('amChartSetor'); if (!el) return;
            const mx = Math.max(...setor.values);
            const bg = setor.values.map(v => v===mx?'#F43F5E':v>=mx*.75?'#F97316':v>=mx*.5?'#F59E0B':'#0EA5E9');
            if (amChartSetor) amChartSetor.destroy();
            amChartSetor = new Chart(el, {
                type:'bar',
                data:{ labels:setor.labels, datasets:[{ label:'Acidentes', data:setor.values, backgroundColor:bg, borderColor:bg, borderWidth:1, borderRadius:5, borderSkipped:false }]},
                options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:{duration:900,easing:'easeOutQuart'},
                    onClick:(evt,elems)=>{ if(elems.length){ amDrilldownSetorBar(elems[0].index); } },
                    plugins:{ legend:{display:false}, tooltip:amTooltipCfg },
                    scales:{ x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{color:'#94A3B8',font:{size:10}},beginAtZero:true}, y:{grid:{display:false},ticks:{color:'#64748B',font:{size:10,weight:'500'}}} },
                },
            });
        }

        function amBuildSpark(id, data, color) {
            const el = amEl(id); if (!el) return;
            const c = el.getContext('2d');
            const g = c.createLinearGradient(0,0,0,46);
            g.addColorStop(0, amRgba(color,0.3)); g.addColorStop(1, amRgba(color,0));
            if (amSparks[id]) amSparks[id].destroy();
            amSparks[id] = new Chart(el, {
                type:'line',
                data:{ labels:data.map((_,i)=>i), datasets:[{ data, borderColor:color, backgroundColor:g, borderWidth:1.8, fill:true, tension:0.45, pointRadius:0 }]},
                options:{ responsive:true, maintainAspectRatio:false, animation:{duration:600}, plugins:{legend:{display:false},tooltip:{enabled:false}}, scales:{x:{display:false},y:{display:false,beginAtZero:true}} },
            });
        }

        /* ══════════════════════════════════════════════════════════
           UPDATE ALL — single function renders everything
           ══════════════════════════════════════════════════════════ */
        function amRenderAll(d) {
            amCurrentData = d;
            const k = d.kpis;

            /* KPIs */
            const setT = (id,v) => { const e=amEl(id); if(e) e.textContent=v; };
            setT('amKpiTotal', k.total);
            setT('amKpiPerf', k.perf);
            setT('amKpiVacc', k.vaccPct + '%');
            setT('amKpiDays', k.days);

            /* KPI deltas */
            const totalD = amEl('amKpiTotalDelta');
            if (totalD) { const down = k.delta <= 0; totalD.className = `am-kpi-delta ${down?'am-delta-down':'am-delta-up'}`; totalD.textContent = `${down?'▼':'▲'} ${Math.abs(k.delta)}% vs período ant.`; }

            const perfD = amEl('amKpiPerfDelta');
            if (perfD) { perfD.className = 'am-kpi-delta am-delta-down'; perfD.textContent = `▼ ${Math.abs(k.delta + 10)}% vs período ant.`; }

            const vaccD = amEl('amKpiVaccDelta');
            if (vaccD) { vaccD.className = 'am-kpi-delta am-delta-up'; vaccD.textContent = `▲ 3% vs mês anterior`; }

            const daysD = amEl('amKpiDaysDelta');
            if (daysD) { daysD.textContent = `Recorde: ${k.record} dias`; daysD.style.background='#F1F5F9'; daysD.style.color='#475569'; }

            /* KPI subs */
            setT('amKpiTotalSub', `${amSum(d.fis)+amSum(d.quim)} físicos/químicos + ${amSum(d.perf)} perf.`);
            setT('amKpiPerfSub', `${k.bio} com exposição biológica`);
            setT('amKpiVaccSub', `${k.vaccUp} de ${k.vaccTotal} colaboradores`);
            setT('amKpiDaysSub', `Período: ${amPeriod === '7d'?'7 dias':amPeriod === '30d'?'30 dias':amPeriod === '90d'?'90 dias':'12 meses'}`);

            /* Gauge stats */
            const gv = document.querySelectorAll('#relatorios .am-gauge-stat-val');
            if (gv[0]) gv[0].textContent = k.vaccUp;
            if (gv[1]) gv[1].textContent = k.vaccPend;
            if (gv[2]) gv[2].textContent = k.vaccOver;

            /* Chart badges */
            const bp = amEl('amBadgePerf');
            if (bp) bp.textContent = `${amSum(d.perf)} no período`;
            const bfq = amEl('amBadgeFQ');
            if (bfq) bfq.textContent = `${amSum(d.fis)+amSum(d.quim)} no período`;

            /* Sparklines (2 remaining) */
            const sk = d.sparks;
            amBuildSpark('amSpark5', sk.bioExp, '#8B5CF6');
            setT('amSparkVal5', amSum(sk.bioExp));
            amBuildSpark('amSpark6', sk.daysNo, '#F59E0B');
            setT('amSparkVal6', sk.daysNo[sk.daysNo.length-1]);

            /* Main charts */
            amBuildPerf(d);
            amBuildFQ(d);
            amBuildDonut(d.donut);
            amBuildSetor(d.setor);
            amAnimateGauge(k.vaccPct);

            /* Dynamic insights */
            amRenderInsights(d);
        }

        /* ══════════════════════════════════════════════════════════
           DYNAMIC INSIGHTS — generated from data
           ══════════════════════════════════════════════════════════ */
        function amRenderInsights(d) {
            const row = amEl('amInsightsRow');
            if (!row) return;
            const k = d.kpis;
            const totalPerf = amSum(d.perf);
            const totalFis = amSum(d.fis);
            const totalQuim = amSum(d.quim);
            const topSetor = d.setor.labels[d.setor.values.indexOf(Math.max(...d.setor.values))];
            const topSetorPct = Math.round((Math.max(...d.setor.values) / (amSum(d.setor.values)||1)) * 100);

            const insights = [];

            if (k.delta < 0) {
                insights.push({ icon:'📉', bg:'#DBEAFE', title:'Redução Consistente', desc:`Queda de ${Math.abs(k.delta)}% nos acidentes totais no período selecionado. Tendência positiva de segurança ocupacional.` });
            } else {
                insights.push({ icon:'📈', bg:'#FEE2E2', title:'Atenção: Alta nos Acidentes', desc:`Aumento de ${k.delta}% nos acidentes no período. Recomenda-se revisão dos protocolos de segurança.` });
            }

            if (k.vaccPct >= 85) {
                const faltam = k.vaccTotal - k.vaccUp;
                insights.push({ icon:'🎯', bg:'#D1FAE5', title:'Meta Vacinal Próxima', desc:`Cobertura em ${k.vaccPct}%. Faltam ${faltam} colaboradores para atingir 93%. ${k.vaccOver} com vacina vencida.` });
            } else {
                insights.push({ icon:'💉', bg:'#FEF3C7', title:'Cobertura Vacinal Baixa', desc:`Apenas ${k.vaccPct}% de cobertura. ${k.vaccOver} colaboradores com vacinas vencidas precisam de atenção urgente.` });
            }

            insights.push({ icon:'⚠️', bg:'#FEF3C7', title:`${topSetor} em Destaque`, desc:`${topSetor} concentra ${topSetorPct}% dos acidentes no período. Físicos: ${totalFis}, Químicos: ${totalQuim}, Perfurocortantes: ${totalPerf}.` });

            row.innerHTML = insights.map(i => `
                <div class="am-insight-card">
                    <div class="am-insight-icon" style="background:${i.bg};">${i.icon}</div>
                    <div>
                        <div class="am-insight-title">${i.title}</div>
                        <div class="am-insight-desc">${i.desc}</div>
                    </div>
                </div>
            `).join('');
        }

        /* ══════════════════════════════════════════════════════════
           DRILL-DOWN — modal with detail chart + table
           ══════════════════════════════════════════════════════════ */
        function amOpenDrilldown(title, buildFn) {
            const overlay = amEl('amDrilldownOverlay');
            amEl('amDdTitle').textContent = title;
            if (amDdChartInst) { amDdChartInst.destroy(); amDdChartInst = null; }
            buildFn();
            overlay.classList.add('open');
            overlay.querySelector('.am-dd-close').focus();
        }

        window.amCloseDrilldown = function() {
            const overlay = amEl('amDrilldownOverlay');
            overlay.classList.remove('open');
            if (amDdChartInst) { amDdChartInst.destroy(); amDdChartInst = null; }
        };

        /* Close on overlay click or Escape */
        document.addEventListener('keydown', e => { if (e.key === 'Escape') amCloseDrilldown(); });
        document.addEventListener('click', e => { if (e.target.id === 'amDrilldownOverlay') amCloseDrilldown(); });

        /* KPI drill-downs */
        window.amDrilldownKpi = function(type) {
            if (!amCurrentData) return;
            const d = amCurrentData;
            const ddMap = {
                totalAccidents: {
                    title: 'Detalhamento — Total de Acidentes',
                    build: () => {
                        const canvas = amEl('amDdChart');
                        amDdChartInst = new Chart(canvas, {
                            type:'bar', data:{ labels:d.labels, datasets:[
                                { label:'Perfurocortantes', data:d.perf, backgroundColor:'#F43F5E', borderRadius:4 },
                                { label:'Físicos', data:d.fis, backgroundColor:'#F97316', borderRadius:4 },
                                { label:'Químicos', data:d.quim, backgroundColor:'#14B8A6', borderRadius:4 },
                            ]},
                            options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'top',labels:{font:{size:11}}},tooltip:amTooltipCfg}, scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,beginAtZero:true}} },
                        });
                        amEl('amDdTable').innerHTML = `<thead><tr><th>Período</th><th>Perf.</th><th>Físicos</th><th>Químicos</th><th>Total</th></tr></thead><tbody>${d.labels.map((l,i)=>`<tr><td>${l}</td><td>${d.perf[i]}</td><td>${d.fis[i]}</td><td>${d.quim[i]}</td><td><strong>${d.perf[i]+d.fis[i]+d.quim[i]}</strong></td></tr>`).join('')}</tbody>`;
                    }
                },
                sharpObjects: {
                    title: 'Detalhamento — Perfurocortantes',
                    build: () => {
                        const canvas = amEl('amDdChart');
                        amDdChartInst = new Chart(canvas, {
                            type:'line', data:{ labels:d.labels, datasets:[
                                { label:'Ocorrências', data:d.perf, borderColor:'#F43F5E', backgroundColor:amRgba('#F43F5E',0.15), fill:true, tension:0.4, pointRadius:5, pointHoverRadius:8, pointBackgroundColor:'#F43F5E', pointBorderColor:'#fff', pointBorderWidth:2, borderWidth:2.5 },
                                { label:'Notificados', data:d.notif, borderColor:'#0EA5E9', backgroundColor:amRgba('#0EA5E9',0.1), fill:true, tension:0.4, pointRadius:4, borderWidth:2 },
                            ]},
                            options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'top'},tooltip:amTooltipCfg}, scales:{y:{beginAtZero:true}} },
                        });
                        amEl('amDdTable').innerHTML = `<thead><tr><th>Período</th><th>Ocorrências</th><th>Notificados</th><th>Taxa Notif.</th></tr></thead><tbody>${d.labels.map((l,i)=>`<tr><td>${l}</td><td>${d.perf[i]}</td><td>${d.notif[i]}</td><td>${d.perf[i]?((d.notif[i]/d.perf[i])*100).toFixed(0)+'%':'—'}</td></tr>`).join('')}</tbody>`;
                    }
                },
                vaccination: {
                    title: 'Detalhamento — Vacinação',
                    build: () => {
                        const canvas = amEl('amDdChart');
                        const k = d.kpis;
                        amDdChartInst = new Chart(canvas, {
                            type:'doughnut', data:{ labels:['Em Dia','Pendentes','Vencidos'], datasets:[{ data:[k.vaccUp,k.vaccPend,k.vaccOver], backgroundColor:['#10B981','#F59E0B','#F43F5E'], borderWidth:3, borderColor:'#fff', borderRadius:4 }]},
                            options:{ responsive:true, maintainAspectRatio:false, cutout:'60%', plugins:{legend:{position:'right'},tooltip:amTooltipCfg} },
                        });
                        amEl('amDdTable').innerHTML = `<thead><tr><th>Status</th><th>Quantidade</th><th>Percentual</th></tr></thead><tbody>
                            <tr><td style="color:#10B981;font-weight:600;">Em Dia</td><td>${k.vaccUp}</td><td>${((k.vaccUp/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                            <tr><td style="color:#F59E0B;font-weight:600;">Pendentes</td><td>${k.vaccPend}</td><td>${((k.vaccPend/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                            <tr><td style="color:#F43F5E;font-weight:600;">Vencidos</td><td>${k.vaccOver}</td><td>${((k.vaccOver/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                            <tr><td><strong>Total</strong></td><td><strong>${k.vaccTotal}</strong></td><td><strong>100%</strong></td></tr>
                        </tbody>`;
                    }
                },
                daysWithout: {
                    title: 'Detalhamento — Dias Sem Acidente',
                    build: () => {
                        const canvas = amEl('amDdChart');
                        const daysData = d.sparks.daysNo;
                        amDdChartInst = new Chart(canvas, {
                            type:'line', data:{ labels:d.labels.slice(0, daysData.length), datasets:[
                                { label:'Dias sem acidente', data:daysData, borderColor:'#F59E0B', backgroundColor:amRgba('#F59E0B',0.15), fill:true, tension:0.35, pointRadius:5, pointHoverRadius:8, pointBackgroundColor:'#F59E0B', pointBorderColor:'#fff', pointBorderWidth:2, borderWidth:2.5 },
                                { label:'Recorde', data:daysData.map(()=>d.kpis.record), borderColor:'#10B981', borderDash:[6,4], borderWidth:1.5, pointRadius:0, fill:false },
                            ]},
                            options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{position:'top'},tooltip:amTooltipCfg}, scales:{y:{beginAtZero:true}} },
                        });
                        amEl('amDdTable').innerHTML = `<thead><tr><th>Métrica</th><th>Valor</th></tr></thead><tbody>
                            <tr><td>Dias atuais sem acidente</td><td><strong>${d.kpis.days}</strong></td></tr>
                            <tr><td>Recorde histórico</td><td><strong>${d.kpis.record} dias</strong></td></tr>
                            <tr><td>Máximo no período</td><td>${Math.max(...daysData)} dias</td></tr>
                            <tr><td>Resets no período</td><td>${daysData.filter(v=>v===0).length} vezes</td></tr>
                        </tbody>`;
                    }
                },
            };
            const cfg = ddMap[type];
            if (cfg) amOpenDrilldown(cfg.title, cfg.build);
        };

        /* Chart card drill-downs */
        window.amDrilldownChart = function(chartType) {
            if (!amCurrentData) return;
            if (chartType === 'perf') amDrilldownKpi('sharpObjects');
            else if (chartType === 'fq') amDrilldownKpi('totalAccidents');
        };

        /* Point drill-down (click on specific data point) */
        function amDrilldownPoint(chartType, idx) {
            if (!amCurrentData) return;
            const d = amCurrentData;
            const label = d.labels[idx];
            amOpenDrilldown(`Detalhamento — ${label}`, () => {
                const canvas = amEl('amDdChart');
                const vals = chartType === 'perf'
                    ? [{ l:'Ocorrências',v:d.perf[idx],c:'#F43F5E' },{ l:'Notificados',v:d.notif[idx],c:'#0EA5E9' }]
                    : [{ l:'Físicos',v:d.fis[idx],c:'#F97316' },{ l:'Químicos',v:d.quim[idx],c:'#14B8A6' }];
                amDdChartInst = new Chart(canvas, {
                    type:'bar', data:{ labels:vals.map(x=>x.l), datasets:[{ data:vals.map(x=>x.v), backgroundColor:vals.map(x=>x.c), borderRadius:6, borderSkipped:false }]},
                    options:{ responsive:true, maintainAspectRatio:false, indexAxis:'y', plugins:{legend:{display:false},tooltip:amTooltipCfg}, scales:{x:{beginAtZero:true}} },
                });
                amEl('amDdTable').innerHTML = `<thead><tr><th>Tipo</th><th>Quantidade</th><th>% do Total</th></tr></thead><tbody>${vals.map(x=>{
                    const tot = vals.reduce((a,v)=>a+v.v,0)||1;
                    return `<tr><td style="color:${x.c};font-weight:600;">${x.l}</td><td>${x.v}</td><td>${((x.v/tot)*100).toFixed(1)}%</td></tr>`;
                }).join('')}<tr><td><strong>Total</strong></td><td><strong>${vals.reduce((a,v)=>a+v.v,0)}</strong></td><td><strong>100%</strong></td></tr></tbody>`;
            });
        }

        /* Donut slice drill-down */
        function amDrilldownDonutSlice(idx) {
            if (!amCurrentData) return;
            const d = amCurrentData;
            const agent = d.donut.labels[idx];
            const val = d.donut.values[idx];
            const tot = amSum(d.donut.values) || 1;
            amOpenDrilldown(`Detalhamento — ${agent}`, () => {
                const canvas = amEl('amDdChart');
                const monthly = d.labels.map(() => Math.round(val / d.labels.length + (Math.random()*2-1)));
                amDdChartInst = new Chart(canvas, {
                    type:'bar', data:{ labels:d.labels, datasets:[{ label:agent, data:monthly, backgroundColor:AGENT_COLORS[agent]||'#8B5CF6', borderRadius:5 }]},
                    options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false},tooltip:amTooltipCfg}, scales:{y:{beginAtZero:true}} },
                });
                amEl('amDdTable').innerHTML = `<thead><tr><th>Métrica</th><th>Valor</th></tr></thead><tbody>
                    <tr><td>Agente</td><td><strong>${agent}</strong></td></tr>
                    <tr><td>Total de ocorrências</td><td>${val}</td></tr>
                    <tr><td>% do total químico</td><td>${((val/tot)*100).toFixed(1)}%</td></tr>
                    <tr><td>Média por período</td><td>${(val/d.labels.length).toFixed(1)}</td></tr>
                </tbody>`;
            });
        }

        /* Setor bar drill-down */
        function amDrilldownSetorBar(idx) {
            if (!amCurrentData) return;
            const d = amCurrentData;
            const setor = d.setor.labels[idx];
            const val = d.setor.values[idx];
            const tot = amSum(d.setor.values) || 1;
            amOpenDrilldown(`Detalhamento — ${setor}`, () => {
                const canvas = amEl('amDdChart');
                const breakdown = [
                    { l:'Perfurocortantes', v:Math.round(val*0.38), c:'#F43F5E' },
                    { l:'Físicos', v:Math.round(val*0.28), c:'#F97316' },
                    { l:'Químicos', v:Math.round(val*0.24), c:'#14B8A6' },
                    { l:'Biológicos', v:Math.round(val*0.10), c:'#8B5CF6' },
                ];
                amDdChartInst = new Chart(canvas, {
                    type:'doughnut', data:{ labels:breakdown.map(b=>b.l), datasets:[{ data:breakdown.map(b=>b.v), backgroundColor:breakdown.map(b=>b.c), borderWidth:3, borderColor:'#fff', borderRadius:4 }]},
                    options:{ responsive:true, maintainAspectRatio:false, cutout:'60%', plugins:{legend:{position:'right'},tooltip:amTooltipCfg} },
                });
                amEl('amDdTable').innerHTML = `<thead><tr><th>Tipo</th><th>Qtd</th><th>%</th></tr></thead><tbody>${breakdown.map(b=>
                    `<tr><td style="color:${b.c};font-weight:600;">${b.l}</td><td>${b.v}</td><td>${((b.v/val)*100).toFixed(0)}%</td></tr>`
                ).join('')}<tr><td><strong>Total ${setor}</strong></td><td><strong>${val}</strong></td><td><strong>${((val/tot)*100).toFixed(0)}% do total</strong></td></tr></tbody>`;
            });
        }

        /* ══════════════════════════════════════════════════════════
           EXPORT — client-side CSV and PDF
           ══════════════════════════════════════════════════════════ */
        window.amExport = function(fmt) {
            if (!amCurrentData) { amToast('Nenhum dado disponível para exportar','warn'); return; }
            const d = amCurrentData;
            if (fmt === 'csv') {
                let csv = 'Período,Perfurocortantes,Notificados,Físicos,Químicos,Total\n';
                d.labels.forEach((l,i) => {
                    csv += `${l},${d.perf[i]},${d.notif[i]},${d.fis[i]},${d.quim[i]},${d.perf[i]+d.fis[i]+d.quim[i]}\n`;
                });
                csv += `\nResumo\n`;
                csv += `Total Acidentes,${d.kpis.total}\nPerfurocortantes,${d.kpis.perf}\nVariação,${d.kpis.delta}%\n`;
                csv += `Cobertura Vacinal,${d.kpis.vaccPct}%\nDias sem Acidente,${d.kpis.days}\n\n`;
                csv += `Setor,Acidentes\n`;
                d.setor.labels.forEach((l,i) => csv += `${l},${d.setor.values[i]}\n`);
                csv += `\nAgente Químico,Quantidade\n`;
                d.donut.labels.forEach((l,i) => csv += `${l},${d.donut.values[i]}\n`);

                const blob = new Blob(['\uFEFF' + csv], {type:'text/csv;charset=utf-8;'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url; a.download = `ucgs-metricas-${amPeriod}-${new Date().toISOString().slice(0,10)}.csv`;
                a.click(); URL.revokeObjectURL(url);
                amToast('CSV exportado com sucesso','success');
            } else {
                /* PDF — generate printable HTML report */
                const k = d.kpis;
                const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>UCGS Relatório — ${amPeriod}</title>
                <style>body{font-family:Inter,system-ui,sans-serif;padding:40px;color:#0F172A;max-width:800px;margin:0 auto;}
                h1{font-size:1.5rem;border-bottom:2px solid #0EA5E9;padding-bottom:8px;}
                .kpi-row{display:flex;gap:16px;margin:20px 0;}
                .kpi{flex:1;padding:16px;border:1px solid #E2E8F0;border-radius:8px;text-align:center;}
                .kpi-val{font-size:1.8rem;font-weight:800;}
                .kpi-lbl{font-size:0.75rem;color:#64748B;text-transform:uppercase;margin-top:4px;}
                table{width:100%;border-collapse:collapse;margin:20px 0;font-size:0.85rem;}
                th{background:#F8FAFC;padding:8px 12px;text-align:left;border-bottom:2px solid #E2E8F0;font-size:0.75rem;text-transform:uppercase;color:#64748B;}
                td{padding:8px 12px;border-bottom:1px solid #E2E8F0;}
                .footer{margin-top:40px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:0.75rem;color:#94A3B8;text-align:center;}
                @media print{body{padding:20px;}}</style></head><body>
                <h1>UCGS — Relatório de Análises e Métricas</h1>
                <p>Período: <strong>${amPeriod === '7d'?'7 dias':amPeriod === '30d'?'30 dias':amPeriod === '90d'?'90 dias':'12 meses'}</strong> · Gerado em: ${new Date().toLocaleDateString('pt-BR')}</p>
                <div class="kpi-row">
                    <div class="kpi"><div class="kpi-val" style="color:#0EA5E9;">${k.total}</div><div class="kpi-lbl">Total Acidentes</div></div>
                    <div class="kpi"><div class="kpi-val" style="color:#F43F5E;">${k.perf}</div><div class="kpi-lbl">Perfurocortantes</div></div>
                    <div class="kpi"><div class="kpi-val" style="color:#10B981;">${k.vaccPct}%</div><div class="kpi-lbl">Cobertura Vacinal</div></div>
                    <div class="kpi"><div class="kpi-val" style="color:#F59E0B;">${k.days}</div><div class="kpi-lbl">Dias sem Acidente</div></div>
                </div>
                <h2>Acidentes por Período</h2>
                <table><thead><tr><th>Período</th><th>Perf.</th><th>Notif.</th><th>Físicos</th><th>Químicos</th><th>Total</th></tr></thead><tbody>
                ${d.labels.map((l,i)=>`<tr><td>${l}</td><td>${d.perf[i]}</td><td>${d.notif[i]}</td><td>${d.fis[i]}</td><td>${d.quim[i]}</td><td><strong>${d.perf[i]+d.fis[i]+d.quim[i]}</strong></td></tr>`).join('')}
                </tbody></table>
                <h2>Acidentes por Setor</h2>
                <table><thead><tr><th>Setor</th><th>Acidentes</th><th>% do Total</th></tr></thead><tbody>
                ${d.setor.labels.map((l,i)=>{const t=amSum(d.setor.values)||1;return `<tr><td>${l}</td><td>${d.setor.values[i]}</td><td>${((d.setor.values[i]/t)*100).toFixed(1)}%</td></tr>`;}).join('')}
                </tbody></table>
                <h2>Distribuição por Agente Químico</h2>
                <table><thead><tr><th>Agente</th><th>Quantidade</th><th>%</th></tr></thead><tbody>
                ${d.donut.labels.map((l,i)=>{const t=amSum(d.donut.values)||1;return `<tr><td>${l}</td><td>${d.donut.values[i]}</td><td>${((d.donut.values[i]/t)*100).toFixed(1)}%</td></tr>`;}).join('')}
                </tbody></table>
                <h2>Vacinação</h2>
                <table><thead><tr><th>Status</th><th>Qtd</th><th>%</th></tr></thead><tbody>
                <tr><td>Em Dia</td><td>${k.vaccUp}</td><td>${((k.vaccUp/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                <tr><td>Pendentes</td><td>${k.vaccPend}</td><td>${((k.vaccPend/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                <tr><td>Vencidos</td><td>${k.vaccOver}</td><td>${((k.vaccOver/k.vaccTotal)*100).toFixed(1)}%</td></tr>
                </tbody></table>
                <div class="footer">UCGS — Universidade + Comunidade + Gestão em Saúde · Gerado automaticamente</div>
                </body></html>`;
                const w = window.open('','_blank','width=900,height=700');
                w.document.write(html);
                w.document.close();
                setTimeout(() => { w.print(); }, 500);
                amToast('Relatório PDF aberto para impressão','success');
            }
        };

        /* Drill-down export */
        window.amExportDrilldown = function() {
            const table = amEl('amDdTable');
            if (!table) return;
            let csv = '';
            table.querySelectorAll('tr').forEach(row => {
                const cells = [...row.querySelectorAll('th,td')].map(c => c.textContent.trim());
                csv += cells.join(',') + '\n';
            });
            const blob = new Blob(['\uFEFF' + csv], {type:'text/csv;charset=utf-8;'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = `ucgs-detalhe-${new Date().toISOString().slice(0,10)}.csv`;
            a.click(); URL.revokeObjectURL(url);
            amToast('Detalhe exportado em CSV','success');
        };

        /* ══════════════════════════════════════════════════════════
           FILTERS
           ══════════════════════════════════════════════════════════ */
        window.amApplyFilters = function() {
            const setor = amEl('amFilterSetor');
            const tipo = amEl('amFilterTipo');
            amFilterSetor = setor ? setor.value : 'all';
            amFilterTipo = tipo ? tipo.value : 'all';

            const badge = amEl('amFilterBadge');
            const hasFilter = amFilterSetor !== 'all' || amFilterTipo !== 'all';
            if (badge) badge.classList.toggle('show', hasFilter);

            amSetLoading(true);
            setTimeout(() => {
                amRenderAll(amGetData(amPeriod));
                amSetLoading(false);
                amToast(hasFilter ? 'Filtros aplicados' : 'Exibindo todos os dados', 'info');
            }, 350);
        };

        window.amResetFilters = function() {
            const setor = amEl('amFilterSetor');
            const tipo = amEl('amFilterTipo');
            const ds = amEl('amDateStart');
            const de = amEl('amDateEnd');
            if (setor) setor.value = 'all';
            if (tipo) tipo.value = 'all';
            if (ds) ds.value = '';
            if (de) de.value = '';
            amFilterSetor = 'all';
            amFilterTipo = 'all';
            const badge = amEl('amFilterBadge');
            if (badge) badge.classList.remove('show');

            amSetLoading(true);
            setTimeout(() => {
                amRenderAll(amGetData(amPeriod));
                amSetLoading(false);
                amToast('Filtros removidos', 'info');
            }, 300);
        };

        /* ── Period switch — now updates EVERYTHING ────────────── */
        window.amSetPeriod = function(btn, period) {
            document.querySelectorAll('.am-period-tab').forEach(t => t.classList.remove('am-active'));
            btn.classList.add('am-active');
            amPeriod = period;
            amSetLoading(true);
            setTimeout(() => {
                amRenderAll(amGetData(period));
                amSetLoading(false);
            }, 300);
        };

        /* ── Init ───────────────────────────────────────────────── */
        function amInit() {
            if (amInitialized) return;
            amInitialized = true;
            amSetLoading(true);
            setTimeout(() => {
                amRenderAll(amGetData(amPeriod));
                amSetLoading(false);
            }, 400);
        }

        document.addEventListener('click', function(e) {
            if (e.target.closest('[data-section="relatorios"]')) setTimeout(amInit, 90);
        });
        if (document.querySelector('#relatorios.active')) setTimeout(amInit, 90);

        /* Keyboard support for KPI cards */
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.target.matches('.am-kpi-card[data-drilldown]')) {
                e.target.click();
            }
        });
    })();

    // ============================================================
    // INIT
    // ============================================================
    renderNotifications();