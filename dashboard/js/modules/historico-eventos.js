// ================================================================
    // HISTÓRICO DE EVENTOS — FULL INTERACTIVITY ENGINE
    // ================================================================
    (function() {
        'use strict';

        var histActiveFilter = 'todos';
        var histCurrentDetailEl = null;

        // ── STATUS MAPPING ──
        var statusMap = {
            'vigente':   { label: 'Vigente',   filterKeys: ['vigente'], dot: '#10B981' },
            'gerado':    { label: 'Gerado',    filterKeys: ['vigente', 'concluido'], dot: '#8B5CF6' },
            'concluído': { label: 'Concluído', filterKeys: ['concluido'], dot: '#10B981' },
            'concluido': { label: 'Concluído', filterKeys: ['concluido'], dot: '#10B981' },
            'pendente':  { label: 'Pendente',  filterKeys: ['pendente'], dot: '#F97316' },
            'urgente':   { label: 'Urgente',   filterKeys: ['vencido', 'pendente'], dot: '#DC2626' },
            'vencido':   { label: 'Vencido',   filterKeys: ['vencido'], dot: '#DC2626' },
            'alta':      { label: 'Alta',       filterKeys: ['vencido', 'pendente'], dot: '#F97316' },
            'média':     { label: 'Média',      filterKeys: ['pendente'], dot: '#0EA5E9' },
            'baixa':     { label: 'Baixa',      filterKeys: ['concluido', 'vigente'], dot: '#10B981' },
            'agendado':  { label: 'Agendado',   filterKeys: ['pendente'], dot: '#64748B' },
            'arquivado': { label: 'Arquivado',  filterKeys: ['concluido'], dot: '#64748B' },
            '89%':       { label: '89%',        filterKeys: ['vigente'], dot: '#F59E0B' },
            '82%':       { label: '82%',        filterKeys: ['pendente'], dot: '#F59E0B' }
        };

        // ── TOAST ──
        window.histToast = function(msg, type) {
            var t = document.getElementById('histToast');
            if (!t) return;
            t.textContent = msg;
            t.className = 'hist-toast ' + (type || 'info');
            // Force reflow
            void t.offsetWidth;
            t.classList.add('show');
            clearTimeout(t._timer);
            t._timer = setTimeout(function() { t.classList.remove('show'); }, 3000);
        };

        // ── TOGGLE CARD EXPAND/COLLAPSE ──
        window.histToggleCard = function(headerEl) {
            var card = headerEl.closest('.hist-category-card');
            if (!card) return;
            var isCollapsed = card.classList.toggle('collapsed');
            headerEl.setAttribute('aria-expanded', isCollapsed ? 'false' : 'true');
        };

        // ── FILTER PILLS ──
        window.histSetFilter = function(pillEl) {
            document.querySelectorAll('.hist-filter-pill').forEach(function(p) { p.classList.remove('active'); });
            pillEl.classList.add('active');
            histActiveFilter = pillEl.getAttribute('data-hist-filter');
            histFilterAll();
        };

        // ── SEARCH + FILTER COMBINED ──
        window.histFilterAll = function() {
            var query = (document.getElementById('histSearchInput').value || '').toLowerCase().trim();
            var items = document.querySelectorAll('#histCategoriesGrid .hist-item');
            var visibleCount = 0;
            var cardVisibility = {};

            items.forEach(function(item) {
                var title = (item.getAttribute('data-hist-title') || '').toLowerCase();
                var author = (item.getAttribute('data-hist-author') || '').toLowerCase();
                var date = (item.getAttribute('data-hist-date') || '').toLowerCase();
                var status = (item.getAttribute('data-hist-status') || '').toLowerCase();
                var category = (item.getAttribute('data-hist-category') || '').toLowerCase();

                // Text search match
                var textMatch = !query || title.indexOf(query) !== -1 || author.indexOf(query) !== -1 || date.indexOf(query) !== -1 || category.indexOf(query) !== -1;

                // Status filter match
                var filterMatch = true;
                if (histActiveFilter !== 'todos') {
                    var mapping = statusMap[status];
                    filterMatch = mapping ? mapping.filterKeys.indexOf(histActiveFilter) !== -1 : false;
                }

                var visible = textMatch && filterMatch;
                item.style.display = visible ? '' : 'none';
                if (visible) visibleCount++;

                // Track per-card visibility
                var card = item.closest('.hist-category-card');
                if (card) {
                    var cardId = card.id;
                    if (!cardVisibility[cardId]) cardVisibility[cardId] = 0;
                    if (visible) cardVisibility[cardId]++;
                }
            });

            // Hide cards with zero visible items
            document.querySelectorAll('#histCategoriesGrid .hist-category-card').forEach(function(card) {
                var count = cardVisibility[card.id] || 0;
                card.style.display = count > 0 ? '' : 'none';
            });

            // Empty state
            var emptyEl = document.getElementById('histEmptyState');
            var gridEl = document.getElementById('histCategoriesGrid');
            if (visibleCount === 0) {
                emptyEl.style.display = '';
                gridEl.style.display = 'none';
            } else {
                emptyEl.style.display = 'none';
                gridEl.style.display = '';
            }
        };

        // ── SHOW DETAIL MODAL ──
        window.histShowDetail = function(itemEl) {
            histCurrentDetailEl = itemEl;
            var title = itemEl.getAttribute('data-hist-title') || 'Sem título';
            var date = itemEl.getAttribute('data-hist-date') || '—';
            var author = itemEl.getAttribute('data-hist-author') || '—';
            var status = itemEl.getAttribute('data-hist-status') || '—';
            var statusClass = itemEl.getAttribute('data-hist-status-class') || 'neutral';
            var category = itemEl.getAttribute('data-hist-category') || '—';
            var desc = itemEl.getAttribute('data-hist-desc') || 'Sem descrição detalhada disponível.';
            var dotColor = itemEl.getAttribute('data-hist-dot') || '#64748B';

            var badgeClassMap = { ok: 'hist-badge-ok', warn: 'hist-badge-warn', danger: 'hist-badge-danger', info: 'hist-badge-info', neutral: 'hist-badge-neutral' };
            var badgeCls = badgeClassMap[statusClass] || 'hist-badge-neutral';

            var body = document.getElementById('histDetailBody');
            body.innerHTML =
                '<div class="hist-modal-field">' +
                    '<div class="hist-modal-label">Título</div>' +
                    '<div class="hist-modal-value" style="font-weight:700;font-size:1rem;">' + histEsc(title) + '</div>' +
                '</div>' +
                '<div class="hist-modal-row">' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">Data</div>' +
                        '<div class="hist-modal-value">' + histEsc(date) + '</div>' +
                    '</div>' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">Responsável</div>' +
                        '<div class="hist-modal-value">' + histEsc(author) + '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="hist-modal-row">' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">Categoria</div>' +
                        '<div class="hist-modal-value">' + histEsc(category) + '</div>' +
                    '</div>' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">Status</div>' +
                        '<div class="hist-modal-status-line">' +
                            '<div class="hist-modal-status-dot" style="background:' + dotColor + ';"></div>' +
                            '<span class="hist-item-badge ' + badgeCls + '">' + histEsc(status) + '</span>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="hist-modal-field" style="margin-top:8px;">' +
                    '<div class="hist-modal-label">Descrição Detalhada</div>' +
                    '<div class="hist-modal-value" style="background:var(--surface-alt);padding:14px;border-radius:var(--radius-sm);border:1px solid var(--border);line-height:1.6;">' + histEsc(desc) + '</div>' +
                '</div>' +
                '<div class="hist-modal-row" style="margin-top:8px;">' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">ID do Registro</div>' +
                        '<div class="hist-modal-value" style="font-family:monospace;font-size:0.8rem;color:var(--text-secondary);">EVT-' + Math.abs(histHashCode(title + date)).toString(16).toUpperCase().slice(0,8) + '</div>' +
                    '</div>' +
                    '<div class="hist-modal-field">' +
                        '<div class="hist-modal-label">Última Atualização</div>' +
                        '<div class="hist-modal-value" style="font-size:0.82rem;color:var(--text-secondary);">' + histEsc(date) + ' às 08:00</div>' +
                    '</div>' +
                '</div>';

            document.getElementById('histDetailOverlay').classList.add('open');
            document.querySelector('#histDetailOverlay .hist-modal-close').focus();
        };

        // ── CLOSE DETAIL MODAL ──
        window.histCloseDetail = function() {
            document.getElementById('histDetailOverlay').classList.remove('open');
            if (histCurrentDetailEl) histCurrentDetailEl.focus();
            histCurrentDetailEl = null;
        };

        // ── DELETE RECORD ──
        window.histDeleteRecord = function() {
            if (!histCurrentDetailEl) return;
            if (!confirm('Tem certeza que deseja excluir este registro?')) return;
            var card = histCurrentDetailEl.closest('.hist-category-card');
            histCurrentDetailEl.style.transition = 'opacity 0.3s, transform 0.3s';
            histCurrentDetailEl.style.opacity = '0';
            histCurrentDetailEl.style.transform = 'translateX(-20px)';
            var el = histCurrentDetailEl;
            setTimeout(function() {
                el.remove();
                histUpdateCounts();
                histFilterAll();
            }, 300);
            histCloseDetail();
            histToast('Registro excluído com sucesso.', 'success');
        };

        // ── PRINT DETAIL ──
        window.histPrintDetail = function() {
            var body = document.getElementById('histDetailBody');
            if (!body) return;
            var w = window.open('', '_blank', 'width=700,height=500');
            w.document.write('<html><head><title>Registro - Impressão</title><style>body{font-family:Inter,sans-serif;padding:32px;color:#0F172A;}h2{margin-bottom:16px;}.field{margin-bottom:12px;}.label{font-size:0.75rem;font-weight:600;color:#64748B;text-transform:uppercase;letter-spacing:0.04em;}.value{font-size:0.9rem;margin-top:2px;}</style></head><body>');
            w.document.write('<h2>Detalhes do Registro</h2>');
            w.document.write(body.innerHTML);
            w.document.write('</body></html>');
            w.document.close();
            w.print();
            histToast('Enviado para impressão.', 'info');
        };

        // ── NEW RECORD MODAL ──
        window.histOpenNewRecord = function() {
            document.getElementById('histNewForm').reset();
            // Pre-fill date with today
            var today = new Date();
            document.getElementById('histNewDate').value = today.toISOString().split('T')[0];
            document.getElementById('histNewOverlay').classList.add('open');
            document.getElementById('histNewTitleInput').focus();
        };

        window.histCloseNewRecord = function() {
            document.getElementById('histNewOverlay').classList.remove('open');
        };

        window.histSaveNewRecord = function() {
            var category = document.getElementById('histNewCategory').value;
            var status = document.getElementById('histNewStatus').value;
            var title = document.getElementById('histNewTitleInput').value.trim();
            var dateVal = document.getElementById('histNewDate').value;
            var author = document.getElementById('histNewAuthor').value.trim();
            var desc = document.getElementById('histNewDesc').value.trim();

            if (!category || !status || !title || !dateVal || !author) {
                histToast('Preencha todos os campos obrigatórios.', 'warning');
                return;
            }

            // Format date to dd/mm/yyyy
            var parts = dateVal.split('-');
            var dateFormatted = parts[2] + '/' + parts[1] + '/' + parts[0];

            // Determine target card
            var cardMap = {
                'Protocolos': 'histCatProtocolos',
                'Relatórios Gerais': 'histCatGerais',
                'Enfermagem': 'histCatEnfermagem',
                'Vacinas': 'histCatVacinas',
                'Acidentes': 'histCatAcidentes'
            };
            var targetCard = document.getElementById(cardMap[category]);
            if (!targetCard) return;

            var list = targetCard.querySelector('.hist-items-list');

            // Determine badge class
            var statusLower = status.toLowerCase();
            var mapping = statusMap[statusLower] || { dot: '#64748B' };
            var dotColor = mapping.dot;
            var badgeClsMap = {
                'vigente': 'hist-badge-ok', 'concluído': 'hist-badge-ok', 'gerado': 'hist-badge-ok',
                'pendente': 'hist-badge-info', 'agendado': 'hist-badge-neutral',
                'urgente': 'hist-badge-danger', 'vencido': 'hist-badge-warn'
            };
            var badgeCls = badgeClsMap[statusLower] || 'hist-badge-neutral';

            // Create new item
            var newItem = document.createElement('div');
            newItem.className = 'hist-item';
            newItem.setAttribute('role', 'listitem');
            newItem.setAttribute('tabindex', '0');
            newItem.setAttribute('onclick', 'histShowDetail(this)');
            newItem.setAttribute('onkeydown', "if(event.key==='Enter'||event.key===' '){event.preventDefault();histShowDetail(this);}");
            newItem.setAttribute('data-hist-title', title);
            newItem.setAttribute('data-hist-date', dateFormatted);
            newItem.setAttribute('data-hist-author', author);
            newItem.setAttribute('data-hist-status', status);
            newItem.setAttribute('data-hist-status-class', badgeCls.replace('hist-badge-', ''));
            newItem.setAttribute('data-hist-category', category);
            newItem.setAttribute('data-hist-desc', desc || 'Registro criado em ' + dateFormatted + ' por ' + author + '.');
            newItem.setAttribute('data-hist-dot', dotColor);

            newItem.innerHTML =
                '<div class="hist-item-dot" style="background:' + dotColor + ';"></div>' +
                '<div class="hist-item-body">' +
                    '<div class="hist-item-title">' + histEsc(title) + '</div>' +
                    '<div class="hist-item-meta">' + histEsc(dateFormatted) + ' · ' + histEsc(author) + '</div>' +
                '</div>' +
                '<span class="hist-item-badge ' + badgeCls + '">' + histEsc(status) + '</span>';

            // Insert at top with animation
            newItem.style.opacity = '0';
            newItem.style.transform = 'translateY(-10px)';
            list.insertBefore(newItem, list.firstChild);
            // Force reflow
            void newItem.offsetWidth;
            newItem.style.transition = 'opacity 0.3s, transform 0.3s';
            newItem.style.opacity = '1';
            newItem.style.transform = 'translateY(0)';

            // Ensure card is expanded
            targetCard.classList.remove('collapsed');
            var header = targetCard.querySelector('.hist-cat-header');
            if (header) header.setAttribute('aria-expanded', 'true');

            histCloseNewRecord();
            histUpdateCounts();
            histToast('Registro criado com sucesso!', 'success');
        };

        // ── EXPORT CSV ──
        window.histExportCSV = function() {
            var items = document.querySelectorAll('#histCategoriesGrid .hist-item');
            if (items.length === 0) {
                histToast('Nenhum registro para exportar.', 'warning');
                return;
            }

            var csv = 'Título;Data;Responsável;Status;Categoria;Descrição\n';
            items.forEach(function(item) {
                if (item.style.display === 'none') return;
                csv += '"' + (item.getAttribute('data-hist-title') || '') + '";';
                csv += '"' + (item.getAttribute('data-hist-date') || '') + '";';
                csv += '"' + (item.getAttribute('data-hist-author') || '') + '";';
                csv += '"' + (item.getAttribute('data-hist-status') || '') + '";';
                csv += '"' + (item.getAttribute('data-hist-category') || '') + '";';
                csv += '"' + (item.getAttribute('data-hist-desc') || '').replace(/"/g, '""') + '"\n';
            });

            var blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'historico_eventos_' + new Date().toISOString().slice(0,10) + '.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            histToast('Exportação CSV concluída!', 'success');
        };

        // ── UPDATE SUMMARY COUNTS ──
        function histUpdateCounts() {
            var items = document.querySelectorAll('#histCategoriesGrid .hist-item');
            var total = 0, ok = 0, pend = 0, crit = 0;

            items.forEach(function(item) {
                total++;
                var status = (item.getAttribute('data-hist-status') || '').toLowerCase();
                var mapping = statusMap[status];
                if (mapping) {
                    if (mapping.filterKeys.indexOf('vigente') !== -1 || mapping.filterKeys.indexOf('concluido') !== -1) ok++;
                    if (mapping.filterKeys.indexOf('pendente') !== -1) pend++;
                    if (mapping.filterKeys.indexOf('vencido') !== -1) crit++;
                }
            });

            var totalEl = document.getElementById('histTotalCount');
            var okEl = document.getElementById('histOkCount');
            var pendEl = document.getElementById('histPendCount');
            var critEl = document.getElementById('histCritCount');
            if (totalEl) totalEl.textContent = total;
            if (okEl) okEl.textContent = ok;
            if (pendEl) pendEl.textContent = pend;
            if (critEl) critEl.textContent = crit;

            // Update card counts
            document.querySelectorAll('#histCategoriesGrid .hist-category-card').forEach(function(card) {
                var count = card.querySelectorAll('.hist-item').length;
                var countEl = card.querySelector('.hist-cat-count');
                if (countEl) countEl.textContent = count + ' registro' + (count !== 1 ? 's' : '');
            });
        }

        // ── ESCAPE KEY — close modals ──
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                var detailOverlay = document.getElementById('histDetailOverlay');
                var newOverlay = document.getElementById('histNewOverlay');
                if (detailOverlay && detailOverlay.classList.contains('open')) {
                    histCloseDetail();
                } else if (newOverlay && newOverlay.classList.contains('open')) {
                    histCloseNewRecord();
                }
            }
        });

        // ── BACKDROP CLICK — close modals ──
        ['histDetailOverlay', 'histNewOverlay'].forEach(function(id) {
            var overlay = document.getElementById(id);
            if (overlay) {
                overlay.addEventListener('click', function(e) {
                    if (e.target === this) {
                        if (id === 'histDetailOverlay') histCloseDetail();
                        else histCloseNewRecord();
                    }
                });
            }
        });

        // ── UTILITY: HTML escape ──
        function histEsc(str) {
            var div = document.createElement('div');
            div.textContent = str;
            return div.innerHTML;
        }

        // ── UTILITY: Simple hash for IDs ──
        function histHashCode(str) {
            var hash = 0;
            for (var i = 0; i < str.length; i++) {
                hash = ((hash << 5) - hash) + str.charCodeAt(i);
                hash |= 0;
            }
            return hash;
        }

        // ── INIT: Update counts from DOM ──
        histUpdateCounts();

    })();