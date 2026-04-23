(function() {
        'use strict';

        /* ══════════════════════════════════════
           1. ESTADO GLOBAL — PACIENTES
           ══════════════════════════════════════ */
        var STORAGE_KEY = 'ucgs_pacientes';
        var PAC_PER_PAGE = 10;
        var pacCurrentPage = 1;
        var pacEditingId = null;

        window.pacStateArray = [];
        function pacLoadState() {
            return window.pacStateArray || [];
        }

        function pacSaveState(list) {
            window.pacStateArray = list;
        }

        // Inicializar com dados de demonstração se vazio
        async function pacFetchSupabase() {
            if (window.PacientesService) {
                try {
                    window.pacStateArray = await window.PacientesService.getPacientes();
                } catch (e) { console.error('Erro Supabase', e); }
            }
            return window.pacStateArray;
        }

        async function pacInitDemo() {
            await pacFetchSupabase();
            pacRenderTable();
        }

        /* ══════════════════════════════════════
           2. GERAÇÃO DE IDs E PRONTUÁRIOS
           ══════════════════════════════════════ */
        function pacNextId(list) {
            var maxNum = 0;
            list.forEach(function(p) {
                var n = parseInt((p.id || '').replace('PAC-', ''), 10);
                if (n > maxNum) maxNum = n;
            });
            return 'PAC-' + String(maxNum + 1).padStart(3, '0');
        }

        function pacNextProntuario(list) {
            var maxNum = 0;
            list.forEach(function(p) {
                var n = parseInt((p.prontuario || '').replace('PRN-', ''), 10);
                if (n > maxNum) maxNum = n;
            });
            return 'PRN-' + String(maxNum + 1).padStart(6, '0');
        }

        /* ══════════════════════════════════════
           3. MASKS — CPF, Telefone, CEP
           ══════════════════════════════════════ */
        window.pacMaskCPF = function(el) {
            var v = el.value.replace(/\D/g, '').slice(0, 11);
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d)/, '$1.$2');
            v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            el.value = v;
        };

        window.pacMaskPhone = function(el) {
            var v = el.value.replace(/\D/g, '').slice(0, 11);
            if (v.length > 6) v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
            else if (v.length > 2) v = v.replace(/(\d{2})(\d+)/, '($1) $2');
            el.value = v;
        };

        window.pacMaskCEP = function(el) {
            var v = el.value.replace(/\D/g, '').slice(0, 8);
            v = v.replace(/(\d{5})(\d)/, '$1-$2');
            el.value = v;
        };

        /* ══════════════════════════════════════
           4. VALIDAÇÃO DE CPF
           ══════════════════════════════════════ */
        function pacValidateCPF(cpf) {
            cpf = cpf.replace(/\D/g, '');
            if (cpf.length !== 11) return false;
            if (/^(\d)\1{10}$/.test(cpf)) return false;
            var sum = 0, rest;
            for (var i = 1; i <= 9; i++) sum += parseInt(cpf[i - 1]) * (11 - i);
            rest = (sum * 10) % 11;
            if (rest === 10 || rest === 11) rest = 0;
            if (rest !== parseInt(cpf[9])) return false;
            sum = 0;
            for (var j = 1; j <= 10; j++) sum += parseInt(cpf[j - 1]) * (12 - j);
            rest = (sum * 10) % 11;
            if (rest === 10 || rest === 11) rest = 0;
            return rest === parseInt(cpf[10]);
        }

        /* ══════════════════════════════════════
           5. RENDERIZAÇÃO — Stats, Tabela, Paginação
           ══════════════════════════════════════ */
        function pacRenderStats(list) {
            var ativos = list.filter(function(p) { return p.status === 'ativo'; }).length;
            var inativos = list.length - ativos;
            var hoje = new Date().toISOString().slice(0, 7);
            var mesAtual = list.filter(function(p) { return (p.dataCadastro || '').slice(0, 7) === hoje; }).length;

            document.getElementById('pacStats').innerHTML =
                '<div class="pac-stat-card">' +
                    '<div class="pac-stat-label">Total de Pacientes</div>' +
                    '<div class="pac-stat-value">' + list.length + '</div>' +
                    '<div class="pac-stat-sub">Base global do sistema</div>' +
                '</div>' +
                '<div class="pac-stat-card">' +
                    '<div class="pac-stat-label">Ativos</div>' +
                    '<div class="pac-stat-value" style="color:var(--success);">' + ativos + '</div>' +
                    '<div class="pac-stat-sub">Em acompanhamento</div>' +
                '</div>' +
                '<div class="pac-stat-card">' +
                    '<div class="pac-stat-label">Inativos</div>' +
                    '<div class="pac-stat-value" style="color:var(--danger);">' + inativos + '</div>' +
                    '<div class="pac-stat-sub">Alta ou transferência</div>' +
                '</div>' +
                '<div class="pac-stat-card">' +
                    '<div class="pac-stat-label">Cadastrados Este Mês</div>' +
                    '<div class="pac-stat-value" style="color:var(--primary);">' + mesAtual + '</div>' +
                    '<div class="pac-stat-sub">' + new Date().toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' }) + '</div>' +
                '</div>';
        }

        function pacGetInitials(nome) {
            var parts = (nome || '').split(' ').filter(Boolean);
            if (parts.length === 0) return '?';
            if (parts.length === 1) return parts[0][0].toUpperCase();
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }

        function pacFormatDate(d) {
            if (!d) return '—';
            var parts = d.split('-');
            if (parts.length === 3) return parts[2] + '/' + parts[1] + '/' + parts[0];
            return d;
        }

        function pacGetFiltered() {
            var list = pacLoadState();
            var q = (document.getElementById('pacSearchInput').value || '').toLowerCase().trim();
            if (!q) return list;
            return list.filter(function(p) {
                return (p.nome || '').toLowerCase().indexOf(q) !== -1 ||
                       (p.cpf || '').indexOf(q) !== -1 ||
                       (p.prontuario || '').toLowerCase().indexOf(q) !== -1;
            });
        }

        function pacRenderTable() {
            var filtered = pacGetFiltered();
            var total = filtered.length;
            var totalPages = Math.max(1, Math.ceil(total / PAC_PER_PAGE));
            if (pacCurrentPage > totalPages) pacCurrentPage = totalPages;

            var start = (pacCurrentPage - 1) * PAC_PER_PAGE;
            var page = filtered.slice(start, start + PAC_PER_PAGE);

            var tbody = document.getElementById('pacTableBody');
            var empty = document.getElementById('pacEmpty');

            if (total === 0) {
                tbody.innerHTML = '';
                empty.style.display = 'block';
            } else {
                empty.style.display = 'none';
                var html = '';
                page.forEach(function(p) {
                    var badgeClass = p.status === 'ativo' ? 'pac-badge-ativo' : 'pac-badge-inativo';
                    var badgeText = p.status === 'ativo' ? 'Ativo' : 'Inativo';
                    var safeId = escapeHtml(p.id);
                    html += '<tr data-pac-id="' + safeId + '" class="pac-row-clickable">' +
                        '<td>' +
                            '<div class="pac-nome-cell">' +
                                '<div class="pac-avatar">' + escapeHtml(pacGetInitials(p.nome)) + '</div>' +
                                '<div>' +
                                    '<div class="pac-nome-text">' + escapeHtml(p.nome || '') + '</div>' +
                                    '<div class="pac-prontuario">' + escapeHtml(p.prontuario || '') + '</div>' +
                                '</div>' +
                            '</div>' +
                        '</td>' +
                        '<td>' + escapeHtml(p.cpf || '—') + '</td>' +
                        '<td>' + escapeHtml(pacFormatDate(p.nascimento)) + '</td>' +
                        '<td>' + escapeHtml(p.telefone || '—') + '</td>' +
                        '<td><span class="pac-badge ' + badgeClass + '">' + badgeText + '</span></td>' +
                        '<td>' +
                            '<div class="pac-actions">' +
                                '<button class="pac-action-btn pac-btn-edit" data-id="' + safeId + '" title="Editar">✏️</button>' +
                                '<button class="pac-action-btn pac-btn-toggle" data-id="' + safeId + '" title="' + (p.status === 'ativo' ? 'Desativar' : 'Ativar') + '">' + (p.status === 'ativo' ? '🚫' : '✅') + '</button>' +
                            '</div>' +
                        '</td>' +
                    '</tr>';
                });
                tbody.innerHTML = html;

                // Event delegation para tabela de pacientes (substitui onclick inline)
                tbody.onclick = function(ev) {
                    var btn = ev.target.closest('.pac-btn-edit');
                    if (btn) { ev.stopPropagation(); pacEdit(btn.dataset.id); return; }
                    var btnToggle = ev.target.closest('.pac-btn-toggle');
                    if (btnToggle) { ev.stopPropagation(); pacToggleStatus(btnToggle.dataset.id); return; }
                    var row = ev.target.closest('tr[data-pac-id]');
                    if (row) pacShowDetail(row.dataset.pacId);
                };
            }

            // Footer
            document.getElementById('pacCountLabel').textContent = total + ' paciente' + (total !== 1 ? 's' : '');

            // Pagination
            var pagEl = document.getElementById('pacPagination');
            var pagHtml = '';
            for (var i = 1; i <= totalPages; i++) {
                pagHtml += '<button class="pac-page-btn' + (i === pacCurrentPage ? ' active' : '') + '" onclick="pacGoPage(' + i + ')">' + i + '</button>';
            }
            pagEl.innerHTML = pagHtml;

            // Update stats
            pacRenderStats(pacLoadState());
        }

        window.pacGoPage = function(n) {
            pacCurrentPage = n;
            pacRenderTable();
        };

        window.pacFilterList = function() {
            pacCurrentPage = 1;
            pacRenderTable();
        };

        /* ══════════════════════════════════════
           6. MODAL — Abrir / Fechar / Salvar
           ══════════════════════════════════════ */
        function pacResetForm() {
            document.getElementById('pacForm').reset();
            ['pacNomeErr', 'pacNascimentoErr', 'pacSexoErr', 'pacCPFErr'].forEach(function(id) {
                document.getElementById(id).classList.remove('visible');
            });
            ['pacNome', 'pacNascimento', 'pacSexo', 'pacCPF'].forEach(function(id) {
                document.getElementById(id).classList.remove('error');
            });
            pacEditingId = null;
        }

        window.pacOpenModal = function(editId) {
            pacResetForm();
            var list = pacLoadState();

            if (editId) {
                pacEditingId = editId;
                var p = list.find(function(x) { return x.id === editId; });
                if (!p) return;
                document.getElementById('pacModalTitle').innerHTML = '✏️ Editar Paciente';
                document.getElementById('pacBtnSave').textContent = 'Atualizar Paciente';
                document.getElementById('pacProntuarioDisplay').textContent = p.prontuario;
                document.getElementById('pacNome').value = p.nome || '';
                document.getElementById('pacNascimento').value = p.nascimento || '';
                document.getElementById('pacSexo').value = p.sexo || '';
                document.getElementById('pacCPF').value = p.cpf || '';
                document.getElementById('pacTelefone').value = p.telefone || '';
                document.getElementById('pacEmail').value = p.email || '';
                document.getElementById('pacLogradouro').value = p.logradouro || '';
                document.getElementById('pacNumero').value = p.numero || '';
                document.getElementById('pacComplemento').value = p.complemento || '';
                document.getElementById('pacBairro').value = p.bairro || '';
                document.getElementById('pacCidade').value = p.cidade || '';
                document.getElementById('pacUF').value = p.uf || '';
                document.getElementById('pacCEP').value = p.cep || '';
                document.getElementById('pacObservacoes').value = p.observacoes || '';
            } else {
                document.getElementById('pacModalTitle').innerHTML = '👤 Novo Paciente';
                document.getElementById('pacBtnSave').textContent = 'Salvar Paciente';
                document.getElementById('pacProntuarioDisplay').textContent = pacNextProntuario(list);
            }

            document.getElementById('pacModalOverlay').classList.add('open');
        };

        window.pacCloseModal = function() {
            document.getElementById('pacModalOverlay').classList.remove('open');
            pacEditingId = null;
        };

        window.pacEdit = function(id) {
            pacOpenModal(id);
        };

        /* ══════════════════════════════════════
           7. VALIDAÇÃO E SAVE
           ══════════════════════════════════════ */
        function pacShowFieldError(inputId, errId) {
            document.getElementById(inputId).classList.add('error');
            document.getElementById(errId).classList.add('visible');
        }
        function pacClearFieldError(inputId, errId) {
            document.getElementById(inputId).classList.remove('error');
            document.getElementById(errId).classList.remove('visible');
        }

        window.pacSave = async function() {
            var valid = true;

            // Nome
            var nome = document.getElementById('pacNome').value.trim();
            if (!nome || nome.length < 3) { pacShowFieldError('pacNome', 'pacNomeErr'); valid = false; }
            else { pacClearFieldError('pacNome', 'pacNomeErr'); }

            // Nascimento
            var nasc = document.getElementById('pacNascimento').value;
            if (!nasc) { pacShowFieldError('pacNascimento', 'pacNascimentoErr'); valid = false; }
            else { pacClearFieldError('pacNascimento', 'pacNascimentoErr'); }

            // Sexo
            var sexo = document.getElementById('pacSexo').value;
            if (!sexo) { pacShowFieldError('pacSexo', 'pacSexoErr'); valid = false; }
            else { pacClearFieldError('pacSexo', 'pacSexoErr'); }

            // CPF
            var cpf = document.getElementById('pacCPF').value;
            var cpfRaw = cpf.replace(/\D/g, '');
            if (!cpfRaw || cpfRaw.length !== 11 || !pacValidateCPF(cpf)) {
                pacShowFieldError('pacCPF', 'pacCPFErr'); valid = false;
            } else {
                // Verificar duplicidade
                var list = pacLoadState();
                var dup = list.find(function(p) { return p.cpf === cpf && p.id !== pacEditingId; });
                if (dup) {
                    document.getElementById('pacCPFErr').textContent = 'CPF já cadastrado para ' + dup.nome;
                    pacShowFieldError('pacCPF', 'pacCPFErr');
                    valid = false;
                } else {
                    document.getElementById('pacCPFErr').textContent = 'CPF inválido';
                    pacClearFieldError('pacCPF', 'pacCPFErr');
                }
            }

            if (!valid) return;

            var list = pacLoadState();

            var patient = {
                nome: nome,
                nascimento: nasc,
                sexo: sexo,
                cpf: cpf,
                telefone: document.getElementById('pacTelefone').value.trim(),
                email: document.getElementById('pacEmail').value.trim(),
                logradouro: document.getElementById('pacLogradouro').value.trim(),
                numero: document.getElementById('pacNumero').value.trim(),
                complemento: document.getElementById('pacComplemento').value.trim(),
                bairro: document.getElementById('pacBairro').value.trim(),
                cidade: document.getElementById('pacCidade').value.trim(),
                uf: document.getElementById('pacUF').value,
                cep: document.getElementById('pacCEP').value.trim(),
                observacoes: document.getElementById('pacObservacoes').value.trim()
            };

            if (pacEditingId) {
                // Update
                var idx = list.findIndex(function(p) { return p.id === pacEditingId; });
                if (idx !== -1) {
                    patient.id = list[idx].id;
                    patient.prontuario = list[idx].prontuario;
                    patient.status = list[idx].status;
                    patient.dataCadastro = list[idx].dataCadastro;
                    list[idx] = patient;
                }
                if(window.PacientesService) { await window.PacientesService.updatePaciente(patient.id, patient); await pacFetchSupabase(); }
                else { pacSaveState(list); }
                pacCloseModal();
                pacShowToast('Paciente atualizado com sucesso', 'success');
            } else {
                // Create
                patient.id = pacNextId(list);
                patient.prontuario = document.getElementById('pacProntuarioDisplay').textContent;
                patient.status = 'ativo';
                patient.dataCadastro = new Date().toISOString();
                list.push(patient);
                if(window.PacientesService) { await window.PacientesService.insertPaciente(patient); await pacFetchSupabase(); }
                else { pacSaveState(list); }
                pacCloseModal();
                pacShowToast('Paciente cadastrado com sucesso', 'success');
            }

            pacRenderTable();
        };

        /* ══════════════════════════════════════
           8. AÇÕES — Toggle Status, Detail
           ══════════════════════════════════════ */
        window.pacToggleStatus = async function(id) {
            var list = pacLoadState();
            var p = list.find(function(x) { return x.id === id; });
            if (!p) return;
            p.status = p.status === 'ativo' ? 'inativo' : 'ativo';
            if(window.PacientesService) { await window.PacientesService.updatePaciente(p.id, { status: p.status }); await pacFetchSupabase(); } else { pacSaveState(list); }
            pacRenderTable();
            pacShowToast('Status alterado para ' + (p.status === 'ativo' ? 'Ativo' : 'Inativo'), 'info');
        };

        window.pacShowDetail = function(id) {
            var list = pacLoadState();
            var p = list.find(function(x) { return x.id === id; });
            if (!p) return;

            var sexoMap = { M: 'Masculino', F: 'Feminino', O: 'Outro' };
            var endereco = [p.logradouro, p.numero, p.complemento, p.bairro, p.cidade, p.uf, p.cep].filter(Boolean).join(', ');

            var html =
                '<div class="pac-detail-row"><span class="pac-detail-key">Prontuário</span><span class="pac-detail-val">' + (p.prontuario || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Nome</span><span class="pac-detail-val">' + (p.nome || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">CPF</span><span class="pac-detail-val">' + (p.cpf || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Nascimento</span><span class="pac-detail-val">' + pacFormatDate(p.nascimento) + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Sexo</span><span class="pac-detail-val">' + (sexoMap[p.sexo] || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Telefone</span><span class="pac-detail-val">' + (p.telefone || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Email</span><span class="pac-detail-val">' + (p.email || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Endereço</span><span class="pac-detail-val">' + (endereco || '—') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Status</span><span class="pac-detail-val"><span class="pac-badge ' + (p.status === 'ativo' ? 'pac-badge-ativo' : 'pac-badge-inativo') + '">' + (p.status === 'ativo' ? 'Ativo' : 'Inativo') + '</span></span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Observações</span><span class="pac-detail-val">' + (p.observacoes || 'Nenhuma') + '</span></div>' +
                '<div class="pac-detail-row"><span class="pac-detail-key">Data Cadastro</span><span class="pac-detail-val">' + new Date(p.dataCadastro).toLocaleDateString('pt-BR') + '</span></div>';

            document.getElementById('pacDetailBody').innerHTML = html;
            document.getElementById('pacDetailOverlay').classList.add('open');
        };

        window.pacCloseDetail = function() {
            document.getElementById('pacDetailOverlay').classList.remove('open');
        };

        /* ══════════════════════════════════════
           9. TOAST
           ══════════════════════════════════════ */
        var pacToastTimer = null;
        function pacShowToast(msg, type) {
            var el = document.getElementById('pacToast');
            el.textContent = msg;
            el.className = 'pac-toast ' + (type || 'info');
            clearTimeout(pacToastTimer);
            requestAnimationFrame(function() { el.classList.add('show'); });
            pacToastTimer = setTimeout(function() { el.classList.remove('show'); }, 3000);
        }

        /* ══════════════════════════════════════
           10. CLOSE OVERLAYS ON BACKDROP CLICK
           ══════════════════════════════════════ */
        document.getElementById('pacModalOverlay').addEventListener('click', function(e) {
            if (e.target === this) pacCloseModal();
        });
        document.getElementById('pacDetailOverlay').addEventListener('click', function(e) {
            if (e.target === this) pacCloseDetail();
        });

        /* ══════════════════════════════════════
           11. KEYBOARD — ESC para fechar modais
           ══════════════════════════════════════ */
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                if (document.getElementById('pacModalOverlay').classList.contains('open')) {
                    pacCloseModal();
                } else if (document.getElementById('pacDetailOverlay').classList.contains('open')) {
                    pacCloseDetail();
                }
            }
        });

        /* ══════════════════════════════════════
           12. INICIALIZAÇÃO
           ══════════════════════════════════════ */
        pacInitDemo();

    })();

    /* ═══════════════════════════════════════════════════════════════
       MÓDULO PRONTUÁRIOS — Prontuário Eletrônico do Paciente
       Prefixo: prt-  |  IIFE isolada
       ═══════════════════════════════════════════════════════════════ */
    (function() {
        'use strict';

        // ============================================================
        // 1. STATE
        // ============================================================
        var prtState = {
            selectedPatientId: null,
            filter: 'todos',
            searchTerm: '',
            timelinePageSize: 8,
            timelineLoaded: 0,
            currentTab: 'timeline',
            debounceTimer: null
        };

        // ============================================================
        // 2. DEMO DATA — Prontuários clínicos simulados
        // ============================================================
        function prtGetPacientes() {
            try {
                var stored = localStorage.getItem('ucgs_pacientes');
                if (stored) {
                    var parsed = JSON.parse(stored);
                    if (Array.isArray(parsed) && parsed.length > 0) return parsed;
                }
            } catch(e) {}
            return prtDemoPacientes();
        }

        function prtDemoPacientes() {
            return [
                { id:'p1', nome:'Maria Silva Santos', cpf:'123.456.789-00', nascimento:'1985-03-15', sexo:'F', telefone:'(11) 99999-1234', prontuario:'PRN-000001', status:'ativo', observacoes:'Hipertensão arterial, Diabetes tipo 2' },
                { id:'p2', nome:'João Pedro Oliveira', cpf:'987.654.321-00', nascimento:'1972-08-22', sexo:'M', telefone:'(11) 98888-5678', prontuario:'PRN-000002', status:'ativo', observacoes:'Asma crônica' },
                { id:'p3', nome:'Ana Beatriz Costa', cpf:'456.789.123-00', nascimento:'1990-11-30', sexo:'F', telefone:'(11) 97777-9012', prontuario:'PRN-000003', status:'ativo', observacoes:'Gestante — 28 semanas' },
                { id:'p4', nome:'Carlos Eduardo Lima', cpf:'321.654.987-00', nascimento:'1965-05-10', sexo:'M', telefone:'(11) 96666-3456', prontuario:'PRN-000004', status:'ativo', observacoes:'Pós-operatório — Artroplastia de joelho D' },
                { id:'p5', nome:'Fernanda Rodrigues', cpf:'654.321.987-00', nascimento:'1998-01-25', sexo:'F', telefone:'(11) 95555-7890', prontuario:'PRN-000005', status:'ativo', observacoes:'Transtorno de ansiedade generalizada' }
            ];
        }

        function prtGetEvolutions(patientId) {
            try {
                var stored = localStorage.getItem('ucgs_prt_evol_' + patientId);
                if (stored) {
                    var parsed = JSON.parse(stored);
                    if (Array.isArray(parsed) && parsed.length > 0) return parsed;
                }
            } catch(e) {}
            return prtDemoEvolutions(patientId);
        }

        function prtSaveEvolutions(patientId, evols) {
            try { localStorage.setItem('ucgs_prt_evol_' + patientId, JSON.stringify(evols)); } catch(e) {}
        }

        function prtDemoEvolutions(pid) {
            var now = Date.now();
            var h = 3600000, d = 86400000;
            var allEvols = {
                'p1': [
                    { id:'e1', tipo:'evolucao', titulo:'Evolução clínica — Controle pressórico', descricao:'Paciente refere melhora dos sintomas de cefaleia. PA aferida: 130/85 mmHg. FC: 72 bpm. Sem queixas respiratórias. Aceitando dieta normossódica. Mantida medicação anti-hipertensiva conforme prescrição.', conduta:'Manter Losartana 50mg 1x/dia. Orientada sobre dieta hipossódica. Retorno em 30 dias com exames de controle.', autor:'Dra. Camila Ferreira', especialidade:'Cardiologia', data: now - 2*h },
                    { id:'e2', tipo:'prescricao', titulo:'Prescrição médica atualizada', descricao:'Losartana Potássica 50mg — 1 comprimido via oral 1x ao dia (manhã). Metformina 850mg — 1 comprimido via oral 2x ao dia (almoço e jantar). Sinvastatina 20mg — 1 comprimido via oral à noite.', conduta:'', autor:'Dra. Camila Ferreira', especialidade:'Cardiologia', data: now - 3*h },
                    { id:'e3', tipo:'exame', titulo:'Resultado — Hemograma completo', descricao:'Hemoglobina: 12.8 g/dL (ref: 12-16). Hematócrito: 38.5%. Leucócitos: 7.200/mm³. Plaquetas: 245.000/mm³. VHS: 15 mm/h. Glicemia de jejum: 142 mg/dL (elevada). HbA1c: 7.2% (acima da meta).', conduta:'Resultados discutidos com paciente. Ajuste de Metformina será avaliado na próxima consulta.', autor:'Lab. Central UCGS', especialidade:'Clínica Geral', data: now - 1*d },
                    { id:'e4', tipo:'enfermagem', titulo:'Anotação de enfermagem — Sinais vitais', descricao:'PA: 128/82 mmHg. FC: 70 bpm. FR: 18 irpm. Tax: 36.4°C. SpO2: 97% AA. Glicemia capilar: 156 mg/dL (pré-almoço). Paciente lúcida, orientada, deambulando sem auxílio. Sem queixas de dor. Aceitação alimentar adequada.', conduta:'Mantidos cuidados de rotina. Comunicado médico sobre glicemia.', autor:'Enf. Juliana Martins', especialidade:'Enfermagem', data: now - 1*d - 4*h },
                    { id:'e5', tipo:'evolucao', titulo:'Avaliação nutricional', descricao:'Paciente com IMC 28.3 (sobrepeso). Circunferência abdominal: 92 cm. Ingestão calórica estimada: 2.100 kcal/dia. Consumo de sódio acima do recomendado. Relata dificuldade em seguir dieta prescrita nos finais de semana.', conduta:'Prescrita dieta de 1.800 kcal, hipossódica, para diabético. Orientações sobre substituições alimentares. Reavaliação em 15 dias.', autor:'Nut. Patrícia Alves', especialidade:'Nutrição', data: now - 2*d },
                    { id:'e6', tipo:'procedimento', titulo:'Eletrocardiograma de repouso', descricao:'ECG de 12 derivações realizado. Ritmo sinusal regular. FC: 68 bpm. Eixo elétrico normal. Sem alterações de ST-T. Intervalo QTc: 420 ms (normal). Laudo: ECG dentro dos limites da normalidade.', conduta:'Resultado anexado ao prontuário. Sem necessidade de intervenção adicional.', autor:'Dr. Roberto Nascimento', especialidade:'Cardiologia', data: now - 3*d },
                    { id:'e7', tipo:'evolucao', titulo:'Consulta de retorno — Endocrinologia', descricao:'Paciente retorna para reavaliação do controle glicêmico. Relata adesão parcial à dieta. Nega episódios de hipoglicemia. Exame físico sem alterações significativas. Pé diabético: sem lesões, pulsos pediais presentes.', conduta:'Aumentar Metformina para 1000mg 2x/dia. Solicitar perfil lipídico, função renal e fundo de olho. Retorno em 60 dias.', autor:'Dr. André Mendes', especialidade:'Clínica Geral', data: now - 5*d },
                    { id:'e8', tipo:'intercorrencia', titulo:'Episódio de hipotensão ortostática', descricao:'Paciente apresentou tontura ao levantar-se do leito às 06:30h. PA deitada: 120/80 mmHg. PA em pé: 90/60 mmHg. FC: 88 bpm. Sem perda de consciência. Orientada a levantar-se gradualmente.', conduta:'Hidratação oral reforçada. Monitorização de PA em 3 posições nas próximas 24h. Avaliar ajuste de anti-hipertensivo se persistir.', autor:'Enf. Juliana Martins', especialidade:'Enfermagem', data: now - 7*d },
                    { id:'e9', tipo:'evolucao', titulo:'Avaliação psicológica inicial', descricao:'Paciente refere ansiedade em relação ao diagnóstico de diabetes. Relata insônia inicial há 3 semanas. Nega ideação suicida. Humor rebaixado, mas responsivo ao acolhimento. Vínculo familiar preservado.', conduta:'Início de acompanhamento psicológico quinzenal. Técnicas de relaxamento e psicoeducação sobre manejo de doença crônica.', autor:'Psic. Renata Campos', especialidade:'Psicologia', data: now - 10*d },
                    { id:'e10', tipo:'exame', titulo:'Perfil lipídico', descricao:'Colesterol total: 218 mg/dL (limítrofe). LDL: 142 mg/dL (elevado). HDL: 45 mg/dL (baixo). Triglicerídeos: 155 mg/dL (limítrofe). VLDL: 31 mg/dL.', conduta:'Manter Sinvastatina 20mg/noite. Reforçar orientações dietéticas e atividade física.', autor:'Lab. Central UCGS', especialidade:'Clínica Geral', data: now - 12*d }
                ],
                'p2': [
                    { id:'e20', tipo:'evolucao', titulo:'Consulta de rotina — Pneumologia', descricao:'Paciente com asma persistente moderada em uso de Budesonida/Formoterol 200/6mcg. Refere 2 crises no último mês, com uso de resgate (Salbutamol) 3x/semana. Ausculta pulmonar com sibilos difusos expiratórios.', conduta:'Aumentar Budesonida para 400mcg. Manter Salbutamol SOS. Espirometria de controle em 30 dias.', autor:'Dr. Ricardo Pinto', especialidade:'Clínica Geral', data: now - 1*d },
                    { id:'e21', tipo:'exame', titulo:'Espirometria', descricao:'VEF1: 72% do previsto (reduzido). CVF: 85% do previsto. VEF1/CVF: 68% (obstrutivo). Prova broncodilatadora: positiva (melhora de 15% no VEF1). Laudo: Distúrbio ventilatório obstrutivo leve a moderado com resposta a broncodilatador.', conduta:'Resultados compatíveis com asma moderada. Ajuste terapêutico realizado.', autor:'Lab. Função Pulmonar', especialidade:'Clínica Geral', data: now - 5*d },
                    { id:'e22', tipo:'enfermagem', titulo:'Educação em saúde — Uso de dispositivo inalatório', descricao:'Realizada orientação sobre técnica correta de uso do dispositivo inalatório. Paciente demonstrou dificuldade inicial com a coordenação mão-pulmão. Após treinamento, demonstrou técnica adequada. Reforçada importância do uso regular da medicação de controle.', conduta:'Agendar reavaliação da técnica em 15 dias.', autor:'Enf. Marcos Silva', especialidade:'Enfermagem', data: now - 6*d }
                ],
                'p3': [
                    { id:'e30', tipo:'evolucao', titulo:'Pré-natal — 28ª semana', descricao:'Gestante G2P1A0 com 28 semanas. Peso: 72kg (ganho de 9kg). PA: 110/70 mmHg. AU: 28cm. BCF: 142 bpm. Movimentação fetal ativa. Sem edema de membros inferiores. Vacinação em dia. Exames do 3º trimestre solicitados.', conduta:'Manter suplementação de ferro e ácido fólico. Retorno em 15 dias. Iniciar contagem de movimentos fetais.', autor:'Dra. Luciana Barros', especialidade:'Clínica Geral', data: now - 2*d },
                    { id:'e31', tipo:'exame', titulo:'Ultrassonografia obstétrica morfológica', descricao:'Feto único, vivo, apresentação cefálica. Biometria compatível com 27 semanas e 5 dias. Peso fetal estimado: 1.050g (percentil 50). Líquido amniótico: ILA 14cm (normal). Placenta: posterior, grau I. Morfologia fetal sem alterações detectáveis.', conduta:'Resultado normal. Manter acompanhamento pré-natal de rotina.', autor:'Dr. Paulo Henrique', especialidade:'Clínica Geral', data: now - 8*d },
                    { id:'e32', tipo:'prescricao', titulo:'Prescrição pré-natal', descricao:'Sulfato ferroso 40mg — 1 comp via oral 1x/dia (longe das refeições). Ácido fólico 5mg — 1 comp via oral 1x/dia. Carbonato de cálcio 500mg — 1 comp via oral 2x/dia.', conduta:'', autor:'Dra. Luciana Barros', especialidade:'Clínica Geral', data: now - 8*d }
                ],
                'p4': [
                    { id:'e40', tipo:'evolucao', titulo:'Evolução pós-operatória — D3', descricao:'Terceiro dia pós-operatório de artroplastia total de joelho direito. Paciente refere dor moderada (EVA 5/10) ao mobilizar. Ferida operatória limpa, sem sinais flogísticos. Dreno retirado. Deambulando com andador com apoio da fisioterapia.', conduta:'Manter analgesia. Iniciar carga parcial progressiva. Crioterapia 3x/dia. Antibioticoprofilaxia até D5.', autor:'Dr. Henrique Campos', especialidade:'Ortopedia', data: now - 1*d },
                    { id:'e41', tipo:'enfermagem', titulo:'Cuidados pós-operatórios', descricao:'Curativo de FO realizado — aspecto limpo e seco. Dreno retirado, débito final: 30mL seroso. PA: 135/80. FC: 78. Tax: 36.8°C. Diurese presente. Aceitando dieta branda. Medicações administradas conforme prescrição.', conduta:'Manter curativos diários. Observar sinais de TVP em MMII.', autor:'Enf. Tatiana Souza', especialidade:'Enfermagem', data: now - 1*d - 6*h },
                    { id:'e42', tipo:'procedimento', titulo:'Sessão de fisioterapia — Mobilização articular', descricao:'Realizada crioterapia por 20 min. Mobilização passiva do joelho D (flexão: 45°, extensão: -5°). Exercícios isométricos de quadríceps. Treino de marcha com andador — percorreu 15 metros. Paciente colaborativo. Boa tolerância.', conduta:'Evoluir para mobilização ativa-assistida amanhã. Objetivo: flexão 60° até D5.', autor:'Ft. Lucas Mendonça', especialidade:'Fisioterapia', data: now - 2*d }
                ],
                'p5': [
                    { id:'e50', tipo:'evolucao', titulo:'Sessão terapêutica — TCC', descricao:'Paciente relata melhora parcial dos sintomas ansiosos após início da medicação (Sertralina 50mg). Ainda apresenta insônia inicial e preocupação excessiva com desempenho acadêmico. Trabalhados registros de pensamentos automáticos e reestruturação cognitiva.', conduta:'Manter sessões semanais. Introduzir técnica de higiene do sono. Diário de pensamentos para próxima sessão.', autor:'Psic. Renata Campos', especialidade:'Psicologia', data: now - 3*d },
                    { id:'e51', tipo:'prescricao', titulo:'Prescrição psiquiátrica', descricao:'Sertralina 50mg — 1 comprimido via oral pela manhã. Melatonina 3mg — 1 comprimido via oral 30 min antes de dormir (uso por 30 dias).', conduta:'Reavaliar resposta em 4 semanas. Paciente orientada sobre efeitos colaterais e tempo de latência do ISRS.', autor:'Dr. Felipe Araújo', especialidade:'Clínica Geral', data: now - 10*d },
                    { id:'e52', tipo:'exame', titulo:'Avaliação laboratorial', descricao:'TSH: 2.8 mUI/L (normal). T4 livre: 1.2 ng/dL (normal). Hemograma sem alterações. Glicemia: 88 mg/dL. Função renal e hepática normais.', conduta:'Exames dentro da normalidade. Excluída causa orgânica para sintomas ansiosos.', autor:'Lab. Central UCGS', especialidade:'Clínica Geral', data: now - 15*d }
                ]
            };
            return allEvols[pid] || [];
        }

        var prtClinicalData = {
            'p1': {
                alergias: ['Dipirona', 'Sulfa'],
                comorbidades: ['Hipertensão Arterial Sistêmica', 'Diabetes Mellitus tipo 2', 'Dislipidemia'],
                tipoSanguineo: 'O+',
                peso: '78 kg',
                altura: '1.62 m',
                imc: '29.7',
                medicacoes: [
                    { nome: 'Losartana 50mg', dose: '1x/dia — manhã' },
                    { nome: 'Metformina 850mg', dose: '2x/dia — almoço e jantar' },
                    { nome: 'Sinvastatina 20mg', dose: '1x/dia — noite' }
                ],
                ultimaConsulta: '28/03/2026',
                proximaConsulta: '27/04/2026'
            },
            'p2': {
                alergias: ['AAS'],
                comorbidades: ['Asma persistente moderada'],
                tipoSanguineo: 'A+',
                peso: '82 kg',
                altura: '1.75 m',
                imc: '26.8',
                medicacoes: [
                    { nome: 'Budesonida/Formoterol 400/6mcg', dose: '2x/dia — manhã e noite' },
                    { nome: 'Salbutamol 100mcg', dose: 'SOS — máx 6 jatos/dia' }
                ],
                ultimaConsulta: '27/03/2026',
                proximaConsulta: '26/04/2026'
            },
            'p3': {
                alergias: [],
                comorbidades: ['Gestação 28 semanas — G2P1A0'],
                tipoSanguineo: 'B+',
                peso: '72 kg',
                altura: '1.68 m',
                imc: '25.5',
                medicacoes: [
                    { nome: 'Sulfato Ferroso 40mg', dose: '1x/dia' },
                    { nome: 'Ácido Fólico 5mg', dose: '1x/dia' },
                    { nome: 'Carbonato de Cálcio 500mg', dose: '2x/dia' }
                ],
                ultimaConsulta: '26/03/2026',
                proximaConsulta: '09/04/2026'
            },
            'p4': {
                alergias: ['Penicilina'],
                comorbidades: ['Osteoartrose de joelho', 'Hipertensão controlada'],
                tipoSanguineo: 'AB+',
                peso: '90 kg',
                altura: '1.78 m',
                imc: '28.4',
                medicacoes: [
                    { nome: 'Tramadol 50mg', dose: '6/6h — SOS dor' },
                    { nome: 'Cefazolina 1g EV', dose: '8/8h — até D5 PO' },
                    { nome: 'Enoxaparina 40mg SC', dose: '1x/dia' }
                ],
                ultimaConsulta: '27/03/2026',
                proximaConsulta: '03/04/2026'
            },
            'p5': {
                alergias: [],
                comorbidades: ['TAG — Transtorno de Ansiedade Generalizada'],
                tipoSanguineo: 'A-',
                peso: '58 kg',
                altura: '1.65 m',
                imc: '21.3',
                medicacoes: [
                    { nome: 'Sertralina 50mg', dose: '1x/dia — manhã' },
                    { nome: 'Melatonina 3mg', dose: '1x/dia — antes de dormir' }
                ],
                ultimaConsulta: '25/03/2026',
                proximaConsulta: '01/04/2026'
            }
        };

        // ============================================================
        // 3. HELPERS
        // ============================================================
        function prtEsc(str) {
            var div = document.createElement('div');
            div.appendChild(document.createTextNode(str || ''));
            return div.innerHTML;
        }

        function prtInitials(name) {
            if (!name) return '??';
            var parts = name.trim().split(/\s+/);
            if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
            return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
        }

        function prtFormatDate(ts) {
            var d = new Date(ts);
            return d.toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit', year:'numeric' });
        }

        function prtFormatDateTime(ts) {
            var d = new Date(ts);
            return d.toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit', year:'numeric' }) +
                   ' às ' + d.toLocaleTimeString('pt-BR', { hour:'2-digit', minute:'2-digit' });
        }

        function prtFormatDateLabel(ts) {
            var d = new Date(ts);
            var today = new Date();
            var yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);

            if (d.toDateString() === today.toDateString()) return 'Hoje';
            if (d.toDateString() === yesterday.toDateString()) return 'Ontem';
            return d.toLocaleDateString('pt-BR', { weekday:'long', day:'numeric', month:'long', year:'numeric' });
        }

        function prtCalcAge(nascimento) {
            if (!nascimento) return '—';
            var birth = new Date(nascimento);
            var today = new Date();
            var age = today.getFullYear() - birth.getFullYear();
            var m = today.getMonth() - birth.getMonth();
            if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
            return age + ' anos';
        }

        function prtDotColor(tipo) {
            var map = { evolucao:'prt-dot-blue', prescricao:'prt-dot-green', exame:'prt-dot-orange', procedimento:'prt-dot-purple', enfermagem:'prt-dot-red', intercorrencia:'prt-dot-red' };
            return map[tipo] || 'prt-dot-blue';
        }

        function prtTypeClass(tipo) {
            var map = { evolucao:'prt-type-evolucao', prescricao:'prt-type-prescricao', exame:'prt-type-exame', procedimento:'prt-type-procedimento', enfermagem:'prt-type-enfermagem', intercorrencia:'prt-type-intercorrencia' };
            return map[tipo] || 'prt-type-evolucao';
        }

        function prtTypeLabel(tipo) {
            var map = { evolucao:'Evolução', prescricao:'Prescrição', exame:'Exame', procedimento:'Procedimento', enfermagem:'Enfermagem', intercorrencia:'Intercorrência' };
            return map[tipo] || tipo;
        }

        function prtShowToast(msg, type) {
            var el = document.getElementById('prtToast');
            el.textContent = msg;
            el.className = 'prt-toast ' + (type || 'info');
            requestAnimationFrame(function() { el.classList.add('show'); });
            setTimeout(function() { el.classList.remove('show'); }, 3000);
        }

        // ============================================================
        // 4. PATIENT LIST RENDERING
        // ============================================================
        function prtRenderPatientList() {
            var pacientes = prtGetPacientes();
            var term = prtState.searchTerm.toLowerCase().trim();
            var filter = prtState.filter;

            var filtered = pacientes.filter(function(p) {
                var matchSearch = !term ||
                    (p.nome || '').toLowerCase().indexOf(term) !== -1 ||
                    (p.cpf || '').indexOf(term) !== -1 ||
                    (p.prontuario || '').toLowerCase().indexOf(term) !== -1;

                var matchFilter = filter === 'todos' || p.status === filter;
                return matchSearch && matchFilter;
            });

            var list = document.getElementById('prtPatientList');
            if (filtered.length === 0) {
                list.innerHTML = '<div class="prt-empty-state" style="padding:40px 20px;">' +
                    '<div class="prt-empty-icon" style="font-size:2rem;">🔍</div>' +
                    '<div class="prt-empty-title" style="font-size:0.9rem;">Nenhum paciente encontrado</div>' +
                    '<div class="prt-empty-desc" style="font-size:0.78rem;">Tente buscar por outro nome ou ajustar os filtros.</div>' +
                    '</div>';
            } else {
                var html = '';
                filtered.forEach(function(p) {
                    var isActive = p.id === prtState.selectedPatientId;
                    var badgeClass = 'prt-badge-ativo';
                    var badgeText = 'Ativo';
                    if (p.status === 'internado') { badgeClass = 'prt-badge-internado'; badgeText = 'Internado'; }
                    else if (p.status === 'alta' || p.status === 'inativo') { badgeClass = 'prt-badge-alta'; badgeText = 'Alta'; }

                    html += '<div class="prt-patient-item' + (isActive ? ' active' : '') + '" data-patient-id="' + prtEsc(p.id) + '">' +
                        '<div class="prt-patient-avatar">' + prtEsc(prtInitials(p.nome)) + '</div>' +
                        '<div class="prt-patient-info">' +
                            '<div class="prt-patient-name">' + prtEsc(p.nome) + '</div>' +
                            '<div class="prt-patient-meta">' +
                                '<span>' + prtEsc(p.prontuario || '') + '</span>' +
                                '<span>' + prtEsc(prtCalcAge(p.nascimento)) + '</span>' +
                            '</div>' +
                        '</div>' +
                        '<span class="prt-patient-badge ' + badgeClass + '">' + badgeText + '</span>' +
                    '</div>';
                });
                list.innerHTML = html;
            }

            document.getElementById('prtSidebarFooter').textContent = filtered.length + ' paciente' + (filtered.length !== 1 ? 's' : '') + ' encontrado' + (filtered.length !== 1 ? 's' : '');
        }

        // ============================================================
        // 5. PATIENT SELECTION
        // ============================================================
        function prtSelectPatient(patientId) {
            prtState.selectedPatientId = patientId;
            prtState.timelineLoaded = 0;
            prtState.currentTab = 'timeline';

            prtRenderPatientList();
            prtRenderPatientHeader();
            prtRenderTimeline();
            prtRenderResumo();
            prtRenderPrescricoes();
            prtRenderExames();

            // Show header, hide empty
            document.getElementById('prtEmptyState').style.display = 'none';
            document.getElementById('prtPatientHeader').style.display = 'block';

            // Reset tabs
            var tabs = document.querySelectorAll('#prtTabs .prt-tab');
            tabs.forEach(function(t) { t.classList.toggle('active', t.dataset.tab === 'timeline'); });
            var panes = document.querySelectorAll('#prtContent .prt-tab-pane');
            panes.forEach(function(p) { p.classList.toggle('active', p.id === 'prtTabTimeline'); });
        }

        function prtRenderPatientHeader() {
            var pacientes = prtGetPacientes();
            var p = pacientes.find(function(x) { return x.id === prtState.selectedPatientId; });
            if (!p) return;

            document.getElementById('prtHeaderAvatar').textContent = prtInitials(p.nome);
            document.getElementById('prtHeaderName').textContent = p.nome;

            var details = '';
            details += '<span class="prt-header-detail"><strong>Prontuário:</strong> ' + prtEsc(p.prontuario || '') + '</span>';
            details += '<span class="prt-header-detail"><strong>Idade:</strong> ' + prtEsc(prtCalcAge(p.nascimento)) + '</span>';
            details += '<span class="prt-header-detail"><strong>Sexo:</strong> ' + prtEsc(p.sexo === 'F' ? 'Feminino' : p.sexo === 'M' ? 'Masculino' : 'Outro') + '</span>';
            details += '<span class="prt-header-detail"><strong>CPF:</strong> ' + prtEsc(p.cpf || '—') + '</span>';
            if (p.telefone) details += '<span class="prt-header-detail"><strong>Tel:</strong> ' + prtEsc(p.telefone) + '</span>';
            document.getElementById('prtHeaderDetails').innerHTML = details;
        }

        // ============================================================
        // 6. TIMELINE RENDERING
        // ============================================================
        function prtRenderTimeline() {
            var evols = prtGetEvolutions(prtState.selectedPatientId);
            evols.sort(function(a, b) { return b.data - a.data; });

            // Summary cards
            var totalEvol = evols.length;
            var lastDate = evols.length > 0 ? prtFormatDate(evols[0].data) : '—';
            var tipos = {};
            evols.forEach(function(e) { tipos[e.tipo] = (tipos[e.tipo] || 0) + 1; });
            var profissionais = {};
            evols.forEach(function(e) { profissionais[e.autor] = true; });

            document.getElementById('prtSummaryCards').innerHTML =
                '<div class="prt-summary-card"><div class="prt-summary-icon">📝</div><div class="prt-summary-label">Total de Registros</div><div class="prt-summary-value">' + totalEvol + '</div><div class="prt-summary-sub">no prontuário</div></div>' +
                '<div class="prt-summary-card"><div class="prt-summary-icon">📅</div><div class="prt-summary-label">Último Registro</div><div class="prt-summary-value">' + lastDate + '</div><div class="prt-summary-sub">data mais recente</div></div>' +
                '<div class="prt-summary-card"><div class="prt-summary-icon">🏷️</div><div class="prt-summary-label">Tipos de Registro</div><div class="prt-summary-value">' + Object.keys(tipos).length + '</div><div class="prt-summary-sub">categorias distintas</div></div>' +
                '<div class="prt-summary-card"><div class="prt-summary-icon">👨‍⚕️</div><div class="prt-summary-label">Profissionais</div><div class="prt-summary-value">' + Object.keys(profissionais).length + '</div><div class="prt-summary-sub">envolvidos no cuidado</div></div>';

            // Timeline entries (lazy loading)
            var pageSize = prtState.timelinePageSize;
            prtState.timelineLoaded += pageSize;
            var visible = evols.slice(0, prtState.timelineLoaded);

            var html = '<div class="prt-timeline">';
            var lastDateLabel = '';

            visible.forEach(function(e) {
                var dateLabel = prtFormatDateLabel(e.data);
                if (dateLabel !== lastDateLabel) {
                    html += '<div class="prt-date-separator"><span>' + prtEsc(dateLabel) + '</span></div>';
                    lastDateLabel = dateLabel;
                }

                html += '<div class="prt-timeline-item">' +
                    '<div class="prt-timeline-dot ' + prtDotColor(e.tipo) + '"></div>' +
                    '<div class="prt-timeline-card">' +
                        '<div class="prt-timeline-header">' +
                            '<span class="prt-timeline-type ' + prtTypeClass(e.tipo) + '">' + prtEsc(prtTypeLabel(e.tipo)) + '</span>' +
                            '<span class="prt-timeline-date">🕒 ' + prtEsc(prtFormatDateTime(e.data)) + '</span>' +
                        '</div>' +
                        '<div class="prt-timeline-title">' + prtEsc(e.titulo) + '</div>' +
                        '<div class="prt-timeline-body">' + prtEsc(e.descricao) + '</div>' +
                        (e.conduta ? '<div class="prt-timeline-body" style="margin-top:8px;padding:10px 12px;background:var(--surface-alt);border-radius:var(--radius-sm);border-left:3px solid var(--primary);"><strong style="color:var(--text-primary);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.03em;">Conduta:</strong><br>' + prtEsc(e.conduta) + '</div>' : '') +
                        '<div class="prt-timeline-footer">' +
                            '<div class="prt-timeline-author">' +
                                '<div class="prt-timeline-author-avatar">' + prtEsc(prtInitials(e.autor)) + '</div>' +
                                '<span><strong>' + prtEsc(e.autor) + '</strong></span>' +
                            '</div>' +
                            '<span class="prt-timeline-specialty">' + prtEsc(e.especialidade) + '</span>' +
                        '</div>' +
                    '</div>' +
                '</div>';
            });

            html += '</div>';
            document.getElementById('prtTimelineContainer').innerHTML = html;

            // Show/hide load more
            document.getElementById('prtLoadMore').style.display = prtState.timelineLoaded < evols.length ? 'block' : 'none';
        }

        window.prtLoadMoreEntries = function() {
            var evols = prtGetEvolutions(prtState.selectedPatientId);
            evols.sort(function(a, b) { return b.data - a.data; });

            prtState.timelineLoaded += prtState.timelinePageSize;
            var visible = evols.slice(0, prtState.timelineLoaded);

            var container = document.getElementById('prtTimelineContainer');
            var timeline = container.querySelector('.prt-timeline');
            if (!timeline) return;

            var lastDateLabel = '';
            var html = '';
            visible.forEach(function(e) {
                var dateLabel = prtFormatDateLabel(e.data);
                if (dateLabel !== lastDateLabel) {
                    html += '<div class="prt-date-separator"><span>' + prtEsc(dateLabel) + '</span></div>';
                    lastDateLabel = dateLabel;
                }
                html += '<div class="prt-timeline-item">' +
                    '<div class="prt-timeline-dot ' + prtDotColor(e.tipo) + '"></div>' +
                    '<div class="prt-timeline-card">' +
                        '<div class="prt-timeline-header">' +
                            '<span class="prt-timeline-type ' + prtTypeClass(e.tipo) + '">' + prtEsc(prtTypeLabel(e.tipo)) + '</span>' +
                            '<span class="prt-timeline-date">🕒 ' + prtEsc(prtFormatDateTime(e.data)) + '</span>' +
                        '</div>' +
                        '<div class="prt-timeline-title">' + prtEsc(e.titulo) + '</div>' +
                        '<div class="prt-timeline-body">' + prtEsc(e.descricao) + '</div>' +
                        (e.conduta ? '<div class="prt-timeline-body" style="margin-top:8px;padding:10px 12px;background:var(--surface-alt);border-radius:var(--radius-sm);border-left:3px solid var(--primary);"><strong style="color:var(--text-primary);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.03em;">Conduta:</strong><br>' + prtEsc(e.conduta) + '</div>' : '') +
                        '<div class="prt-timeline-footer">' +
                            '<div class="prt-timeline-author">' +
                                '<div class="prt-timeline-author-avatar">' + prtEsc(prtInitials(e.autor)) + '</div>' +
                                '<span><strong>' + prtEsc(e.autor) + '</strong></span>' +
                            '</div>' +
                            '<span class="prt-timeline-specialty">' + prtEsc(e.especialidade) + '</span>' +
                        '</div>' +
                    '</div>' +
                '</div>';
            });

            timeline.innerHTML = html;
            document.getElementById('prtLoadMore').style.display = prtState.timelineLoaded < evols.length ? 'block' : 'none';
        };

        // ============================================================
        // 7. RESUMO CLÍNICO TAB
        // ============================================================
        function prtRenderResumo() {
            var pid = prtState.selectedPatientId;
            var data = prtClinicalData[pid];
            var pacientes = prtGetPacientes();
            var p = pacientes.find(function(x) { return x.id === pid; });
            if (!data || !p) {
                document.getElementById('prtResumoContent').innerHTML = '<div class="prt-empty-state" style="padding:40px;"><div class="prt-empty-icon">📋</div><div class="prt-empty-title">Sem dados clínicos</div></div>';
                return;
            }

            var html = '<div class="prt-clinical-grid">';

            // Dados pessoais
            html += '<div class="prt-clinical-card">' +
                '<div class="prt-clinical-title">👤 Identificação</div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Nome</span><span class="prt-clinical-val">' + prtEsc(p.nome) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">CPF</span><span class="prt-clinical-val">' + prtEsc(p.cpf) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Nascimento</span><span class="prt-clinical-val">' + prtEsc(prtFormatDate(new Date(p.nascimento).getTime())) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Idade</span><span class="prt-clinical-val">' + prtEsc(prtCalcAge(p.nascimento)) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Sexo</span><span class="prt-clinical-val">' + prtEsc(p.sexo === 'F' ? 'Feminino' : p.sexo === 'M' ? 'Masculino' : 'Outro') + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Tipo Sanguíneo</span><span class="prt-clinical-val">' + prtEsc(data.tipoSanguineo) + '</span></div>' +
            '</div>';

            // Dados antropométricos
            html += '<div class="prt-clinical-card">' +
                '<div class="prt-clinical-title">📏 Dados Antropométricos</div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Peso</span><span class="prt-clinical-val">' + prtEsc(data.peso) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Altura</span><span class="prt-clinical-val">' + prtEsc(data.altura) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">IMC</span><span class="prt-clinical-val">' + prtEsc(data.imc) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Última Consulta</span><span class="prt-clinical-val">' + prtEsc(data.ultimaConsulta) + '</span></div>' +
                '<div class="prt-clinical-row"><span class="prt-clinical-key">Próxima Consulta</span><span class="prt-clinical-val">' + prtEsc(data.proximaConsulta) + '</span></div>' +
            '</div>';

            // Alergias
            html += '<div class="prt-clinical-card">' +
                '<div class="prt-clinical-title">⚠️ Alergias</div>';
            if (data.alergias.length > 0) {
                html += '<div style="display:flex;flex-wrap:wrap;gap:4px;">';
                data.alergias.forEach(function(a) {
                    html += '<span class="prt-allergy-tag">⚠️ ' + prtEsc(a) + '</span>';
                });
                html += '</div>';
            } else {
                html += '<div style="font-size:0.82rem;color:var(--success);font-weight:500;padding:8px 0;">✅ Sem alergias conhecidas</div>';
            }
            html += '<div class="prt-clinical-title" style="margin-top:16px;">🩺 Comorbidades</div>';
            if (data.comorbidades.length > 0) {
                data.comorbidades.forEach(function(c) {
                    html += '<div class="prt-clinical-row"><span class="prt-clinical-val" style="text-align:left;max-width:100%;">• ' + prtEsc(c) + '</span></div>';
                });
            } else {
                html += '<div style="font-size:0.82rem;color:var(--text-secondary);padding:8px 0;">Nenhuma comorbidade registrada</div>';
            }
            html += '</div>';

            // Medicações em uso
            html += '<div class="prt-clinical-card">' +
                '<div class="prt-clinical-title">💊 Medicações em Uso</div>';
            if (data.medicacoes.length > 0) {
                data.medicacoes.forEach(function(m) {
                    html += '<div class="prt-med-item"><span class="prt-med-name">' + prtEsc(m.nome) + '</span><span class="prt-med-dose">' + prtEsc(m.dose) + '</span></div>';
                });
            } else {
                html += '<div style="font-size:0.82rem;color:var(--text-secondary);padding:8px 0;">Nenhuma medicação registrada</div>';
            }
            html += '</div>';

            html += '</div>'; // close grid

            // Observações clínicas
            if (p.observacoes) {
                html += '<div class="prt-clinical-card" style="margin-top:0;">' +
                    '<div class="prt-clinical-title">📝 Observações Clínicas</div>' +
                    '<div style="font-size:0.84rem;color:var(--text-secondary);line-height:1.6;">' + prtEsc(p.observacoes) + '</div>' +
                '</div>';
            }

            document.getElementById('prtResumoContent').innerHTML = html;
        }

        // ============================================================
        // 8. PRESCRIÇÕES TAB
        // ============================================================
        function prtRenderPrescricoes() {
            var evols = prtGetEvolutions(prtState.selectedPatientId);
            var prescricoes = evols.filter(function(e) { return e.tipo === 'prescricao'; });
            prescricoes.sort(function(a, b) { return b.data - a.data; });

            if (prescricoes.length === 0) {
                document.getElementById('prtPrescricoesContent').innerHTML = '<div class="prt-empty-state" style="padding:40px;"><div class="prt-empty-icon">💊</div><div class="prt-empty-title">Nenhuma prescrição registrada</div><div class="prt-empty-desc">As prescrições serão exibidas aqui conforme forem adicionadas.</div></div>';
                return;
            }

            var html = '<div class="prt-timeline">';
            prescricoes.forEach(function(e) {
                html += '<div class="prt-timeline-item">' +
                    '<div class="prt-timeline-dot prt-dot-green"></div>' +
                    '<div class="prt-timeline-card">' +
                        '<div class="prt-timeline-header">' +
                            '<span class="prt-timeline-type prt-type-prescricao">Prescrição</span>' +
                            '<span class="prt-timeline-date">🕒 ' + prtEsc(prtFormatDateTime(e.data)) + '</span>' +
                        '</div>' +
                        '<div class="prt-timeline-title">' + prtEsc(e.titulo) + '</div>' +
                        '<div class="prt-timeline-body" style="white-space:pre-line;">' + prtEsc(e.descricao) + '</div>' +
                        '<div class="prt-timeline-footer">' +
                            '<div class="prt-timeline-author"><div class="prt-timeline-author-avatar">' + prtEsc(prtInitials(e.autor)) + '</div><span><strong>' + prtEsc(e.autor) + '</strong></span></div>' +
                            '<span class="prt-timeline-specialty">' + prtEsc(e.especialidade) + '</span>' +
                        '</div>' +
                    '</div></div>';
            });
            html += '</div>';
            document.getElementById('prtPrescricoesContent').innerHTML = html;
        }

        // ============================================================
        // 9. EXAMES TAB
        // ============================================================
        function prtRenderExames() {
            var evols = prtGetEvolutions(prtState.selectedPatientId);
            var exames = evols.filter(function(e) { return e.tipo === 'exame'; });
            exames.sort(function(a, b) { return b.data - a.data; });

            if (exames.length === 0) {
                document.getElementById('prtExamesContent').innerHTML = '<div class="prt-empty-state" style="padding:40px;"><div class="prt-empty-icon">🔬</div><div class="prt-empty-title">Nenhum exame registrado</div><div class="prt-empty-desc">Os resultados de exames serão exibidos aqui.</div></div>';
                return;
            }

            var html = '<div class="prt-timeline">';
            exames.forEach(function(e) {
                html += '<div class="prt-timeline-item">' +
                    '<div class="prt-timeline-dot prt-dot-orange"></div>' +
                    '<div class="prt-timeline-card">' +
                        '<div class="prt-timeline-header">' +
                            '<span class="prt-timeline-type prt-type-exame">Exame</span>' +
                            '<span class="prt-timeline-date">🕒 ' + prtEsc(prtFormatDateTime(e.data)) + '</span>' +
                        '</div>' +
                        '<div class="prt-timeline-title">' + prtEsc(e.titulo) + '</div>' +
                        '<div class="prt-timeline-body">' + prtEsc(e.descricao) + '</div>' +
                        (e.conduta ? '<div class="prt-timeline-body" style="margin-top:8px;padding:10px 12px;background:var(--surface-alt);border-radius:var(--radius-sm);border-left:3px solid var(--warning);"><strong style="color:var(--text-primary);font-size:0.75rem;">PARECER:</strong><br>' + prtEsc(e.conduta) + '</div>' : '') +
                        '<div class="prt-timeline-footer">' +
                            '<div class="prt-timeline-author"><div class="prt-timeline-author-avatar">' + prtEsc(prtInitials(e.autor)) + '</div><span><strong>' + prtEsc(e.autor) + '</strong></span></div>' +
                            '<span class="prt-timeline-specialty">' + prtEsc(e.especialidade) + '</span>' +
                        '</div>' +
                    '</div></div>';
            });
            html += '</div>';
            document.getElementById('prtExamesContent').innerHTML = html;
        }

        // ============================================================
        // 10. TAB SWITCHING
        // ============================================================
        window.prtSwitchTab = function(tabId, el) {
            prtState.currentTab = tabId;
            document.querySelectorAll('#prtTabs .prt-tab').forEach(function(t) { t.classList.toggle('active', t.dataset.tab === tabId); });
            document.querySelectorAll('#prtContent .prt-tab-pane').forEach(function(p) { p.classList.toggle('active', p.id === 'prtTab' + tabId.charAt(0).toUpperCase() + tabId.slice(1)); });
        };

        // ============================================================
        // 11. FILTER PATIENTS
        // ============================================================
        window.prtFilterPatients = function(filter, el) {
            prtState.filter = filter;
            document.querySelectorAll('.prt-filter-btn').forEach(function(b) { b.classList.toggle('active', b.dataset.filter === filter); });
            prtRenderPatientList();
        };

        // ============================================================
        // 12. SEARCH WITH DEBOUNCE
        // ============================================================
        var prtSearchInput = document.getElementById('prtSearchInput');
        if (prtSearchInput) {
            prtSearchInput.addEventListener('input', function() {
                clearTimeout(prtState.debounceTimer);
                var val = this.value;
                prtState.debounceTimer = setTimeout(function() {
                    prtState.searchTerm = val;
                    prtRenderPatientList();
                }, 250);
            });
        }

        // ============================================================
        // 13. PATIENT LIST CLICK HANDLER (event delegation)
        // ============================================================
        var prtPatientListEl = document.getElementById('prtPatientList');
        if (prtPatientListEl) {
            prtPatientListEl.addEventListener('click', function(e) {
                var item = e.target.closest('.prt-patient-item');
                if (!item) return;
                var pid = item.dataset.patientId;
                if (pid) prtSelectPatient(pid);
            });
        }

        // ============================================================
        // 14. NEW EVOLUTION MODAL
        // ============================================================
        window.prtNewEvolution = function() {
            if (!prtState.selectedPatientId) return;
            document.getElementById('prtEvolForm').reset();
            document.getElementById('prtEvolModalOverlay').classList.add('open');
        };

        window.prtCloseEvolModal = function() {
            document.getElementById('prtEvolModalOverlay').classList.remove('open');
        };

        window.prtSaveEvolution = function() {
            var tipo = document.getElementById('prtEvolTipo').value;
            var titulo = document.getElementById('prtEvolTitulo').value.trim();
            var descricao = document.getElementById('prtEvolDescricao').value.trim();
            var conduta = document.getElementById('prtEvolConduta').value.trim();
            var especialidade = document.getElementById('prtEvolEspecialidade').value;

            if (!tipo || !titulo || !descricao) {
                prtShowToast('Preencha todos os campos obrigatórios.', 'warning');
                return;
            }

            var evols = prtGetEvolutions(prtState.selectedPatientId);
            var newEvol = {
                id: 'e' + Date.now(),
                tipo: tipo,
                titulo: titulo,
                descricao: descricao,
                conduta: conduta,
                autor: 'Guilherme Ferreira',
                especialidade: especialidade,
                data: Date.now()
            };

            evols.unshift(newEvol);
            prtSaveEvolutions(prtState.selectedPatientId, evols);

            prtCloseEvolModal();
            prtState.timelineLoaded = 0;
            prtRenderTimeline();
            prtRenderPrescricoes();
            prtRenderExames();
            prtShowToast('Evolução salva com sucesso!', 'info');
        };

        // ============================================================
        // 15. PRINT
        // ============================================================
        window.prtPrint = function() {
            window.print();
        };

        // ============================================================
        // 16. ESC KEY — close evolution modal
        // ============================================================
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                var overlay = document.getElementById('prtEvolModalOverlay');
                if (overlay && overlay.classList.contains('open')) {
                    prtCloseEvolModal();
                }
            }
        });

        // Backdrop click to close
        var prtEvolOverlay = document.getElementById('prtEvolModalOverlay');
        if (prtEvolOverlay) {
            prtEvolOverlay.addEventListener('click', function(e) {
                if (e.target === this) prtCloseEvolModal();
            });
        }

        // ============================================================
        // 17. INITIALIZATION
        // ============================================================
        prtRenderPatientList();

    })();