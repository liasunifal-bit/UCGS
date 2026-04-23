(function() {
        'use strict';

        /* ── Open/Close Fullscreen ── */
        window.ftOpenFullscreen = function() {
            var el = document.getElementById('ftFullscreen');
            if (!el) return;
            el.classList.add('open');
            document.body.style.overflow = 'hidden';
            ftInitCharts();
        };

        window.ftCloseFullscreen = function() {
            var el = document.getElementById('ftFullscreen');
            if (!el) return;
            el.classList.remove('open');
            document.body.style.overflow = '';
        };

        /* ── Auto-open on nav click ── */
        var ftNav = document.querySelector('.nav-item[data-section="fisioterapia"]');
        if (ftNav) {
            ftNav.addEventListener('click', function() {
                setTimeout(function() { ftOpenFullscreen(); }, 120);
            });
        }

        /* ── Escape to close ── */
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                var cm = document.getElementById('ftConfirmModal');
                if (cm && cm.classList.contains('open')) { ftCloseConfirm(); return; }
                var fs = document.getElementById('ftFullscreen');
                if (fs && fs.classList.contains('open')) ftCloseFullscreen();
            }
        });

        /* ── Sidebar Navigation ── */
        window.ftNavigate = function(el) {
            document.querySelectorAll('.ft-nav-item').forEach(function(n) { n.classList.remove('active'); });
            el.classList.add('active');
            var target = el.getAttribute('data-ft-panel');
            document.querySelectorAll('.ft-panel').forEach(function(p) { p.classList.remove('active'); });
            var panel = document.getElementById(target);
            if (panel) panel.classList.add('active');
            // Reinit charts if evolution panel
            if (target === 'ft-evolucao') setTimeout(ftInitCharts, 100);
            // Close mobile sidebar
            var sb = document.getElementById('ftSidebar');
            var ov = document.getElementById('ftSidebarOverlay');
            if (sb) sb.classList.remove('mobile-open');
            if (ov) ov.classList.remove('open');
        };

        /* ── Mobile Sidebar Toggle ── */
        window.ftToggleSidebar = function() {
            var sb = document.getElementById('ftSidebar');
            var ov = document.getElementById('ftSidebarOverlay');
            if (!sb) return;
            var open = sb.classList.contains('mobile-open');
            sb.classList.toggle('mobile-open', !open);
            if (ov) ov.classList.toggle('open', !open);
        };

        /* ── EVA Scale Update ── */
        window.ftUpdateScale = function(inputId, valId) {
            var inp = document.getElementById(inputId);
            var val = document.getElementById(valId);
            if (!inp || !val) return;
            var v = parseInt(inp.value);
            val.textContent = v;
            val.className = 'ft-scale-value ' + (v <= 3 ? 'low' : v <= 6 ? 'mid' : 'high');
        };

        /* ── Goniometry Deficit Calculator ── */
        window.ftCalcDeficit = function() {
            var pairs = [
                { input: 'ftGonFlex', normal: 80, out: 'ftDefFlex', label: '' },
                { input: 'ftGonExt', normal: 30, out: 'ftDefExt', label: '' },
                { input: 'ftGonFlexQD', normal: 120, out: 'ftDefFlexQ', label: 'D: ' },
                { input: 'ftGonRotD', normal: 45, out: 'ftDefRot', label: 'D: ' }
            ];
            pairs.forEach(function(p) {
                var el = document.getElementById(p.input);
                var out = document.getElementById(p.out);
                if (!el || !out) return;
                var v = parseInt(el.value) || 0;
                var d = v - p.normal;
                var cls = d >= 0 ? 'ft-badge-green' : (d >= -20 ? 'ft-badge-amber' : 'ft-badge-red');
                out.innerHTML = '<span class="ft-badge ' + cls + '">' + p.label + (d >= 0 ? '+' : '') + d + '°</span>';
            });
        };

        /* ── Exercise Selection ── */
        window.ftToggleExercise = function(el) {
            el.classList.toggle('selected');
        };

        window.ftFilterExercises = function(q) {
            q = q.toLowerCase();
            document.querySelectorAll('#ftExerciseBank .ft-exercise-card').forEach(function(c) {
                var name = (c.getAttribute('data-name') || '').toLowerCase();
                c.style.display = name.includes(q) ? '' : 'none';
            });
        };

        /* ── Checkbox Toggle ── */
        window.ftToggleCheck = function(el) {
            el.classList.toggle('checked');
            var dot = el.querySelector('.ft-check-dot');
            if (dot) dot.innerHTML = el.classList.contains('checked') ? '✓' : '';
        };

        /* ── Confirm Save (double confirmation) ── */
        window.ftConfirmSave = function() {
            document.getElementById('ftConfirmModal').classList.add('open');
        };
        window.ftCloseConfirm = function() {
            document.getElementById('ftConfirmModal').classList.remove('open');
        };
        window.ftDoSave = function() {
            ftCloseConfirm();
            ftShowToast('success', '✓ Plano de Tratamento salvo com sucesso!');
        };

        /* ── Toast ── */
        window.ftShowToast = function(type, msg) {
            var t = document.getElementById('ftToast');
            if (!t) return;
            t.className = 'ft-toast show ' + type;
            t.innerHTML = msg;
            setTimeout(function() { t.classList.remove('show'); }, 3500);
        };

        /* ── Print ── */
        window.ftPrint = function() {
            window.print();
        };

        /* ── Charts (Recharts-like via Chart.js) ── */
        var ftChartsInitialized = false;
        function ftInitCharts() {
            if (ftChartsInitialized) return;
            if (typeof Chart === 'undefined') return;
            ftChartsInitialized = true;

            var sessions = ['S5','S6','S7','S8','S9','S10','S11','S12'];
            var gridColor = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#E2E8F0';
            var textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary').trim() || '#64748B';

            var defaults = {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: { legend: { position: 'bottom', labels: { color: textColor, font: { family: 'Inter', size: 11 }, usePointStyle: true, pointStyle: 'circle', padding: 16 } } },
                scales: {
                    x: { grid: { color: gridColor + '40' }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } },
                    y: { grid: { color: gridColor + '40' }, ticks: { color: textColor, font: { family: 'Inter', size: 11 } } }
                }
            };

            // Pain Chart
            var c1 = document.getElementById('ftChartDor');
            if (c1) {
                c1.parentElement.style.height = '280px';
                new Chart(c1, {
                    type: 'line', data: {
                        labels: sessions,
                        datasets: [
                            { label: 'EVA Pré-Sessão', data: [9,9,8,8,7,8,7,7], borderColor: '#DC2626', backgroundColor: 'rgba(220,38,38,0.1)', fill: true, tension: 0.4, pointRadius: 5, pointHoverRadius: 7 },
                            { label: 'EVA Pós-Sessão', data: [7,6,6,5,4,5,5,4], borderColor: '#059669', backgroundColor: 'rgba(5,150,105,0.1)', fill: true, tension: 0.4, pointRadius: 5, pointHoverRadius: 7 }
                        ]
                    }, options: Object.assign({}, defaults, { scales: Object.assign({}, defaults.scales, { y: Object.assign({}, defaults.scales.y, { min: 0, max: 10, title: { display: true, text: 'Intensidade (0-10)', color: textColor } }) }) })
                });
            }

            // ADM Chart
            var c2 = document.getElementById('ftChartADM');
            if (c2) {
                c2.parentElement.style.height = '280px';
                new Chart(c2, {
                    type: 'line', data: {
                        labels: sessions,
                        datasets: [
                            { label: 'Flexão de Tronco (°)', data: [30,32,35,38,40,40,43,45], borderColor: '#0EA5E9', backgroundColor: 'rgba(14,165,233,0.1)', fill: true, tension: 0.4, pointRadius: 5, pointHoverRadius: 7 },
                            { label: 'Flexão Quadril D (°)', data: [75,78,80,82,85,85,88,90], borderColor: '#7C3AED', backgroundColor: 'rgba(124,58,237,0.1)', fill: true, tension: 0.4, pointRadius: 5, pointHoverRadius: 7 }
                        ]
                    }, options: Object.assign({}, defaults, { scales: Object.assign({}, defaults.scales, { y: Object.assign({}, defaults.scales.y, { title: { display: true, text: 'Graus (°)', color: textColor } }) }) })
                });
            }

            // Strength Chart
            var c3 = document.getElementById('ftChartForca');
            if (c3) {
                c3.parentElement.style.height = '280px';
                new Chart(c3, {
                    type: 'bar', data: {
                        labels: ['Quadríceps D','Glúteo Máx D','Paravertebrais','Core','Tibial Ant D'],
                        datasets: [
                            { label: 'Avaliação Inicial', data: [3,2.5,2.5,2,3], backgroundColor: 'rgba(220,38,38,0.6)', borderColor: '#DC2626', borderWidth: 1, borderRadius: 4 },
                            { label: 'Atual', data: [4,3.5,3.5,3,4], backgroundColor: 'rgba(5,150,105,0.6)', borderColor: '#059669', borderWidth: 1, borderRadius: 4 }
                        ]
                    }, options: Object.assign({}, defaults, { scales: Object.assign({}, defaults.scales, { y: Object.assign({}, defaults.scales.y, { min: 0, max: 5, title: { display: true, text: 'Escala Daniels (0-5)', color: textColor } }) }) })
                });
            }
        }

    })();