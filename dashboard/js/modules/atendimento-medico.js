// ============================================================
    // ATENDIMENTO MÉDICO — JavaScript
    // ============================================================
    (function() {

        // Open overlay
        window.atdOpen = function() {
            var overlay = document.getElementById('atdOverlay');
            overlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        };

        // Close overlay
        window.atdClose = function() {
            var overlay = document.getElementById('atdOverlay');
            overlay.classList.remove('open');
            document.body.style.overflow = '';
            // Restore active nav item to dashboard
            document.querySelectorAll('.nav-item').forEach(function(i) { i.classList.remove('active'); });
            var dashNav = document.querySelector('.nav-item[data-section="dashboard"]');
            if (dashNav) dashNav.classList.add('active');
        };

        // Tab switching
        window.atdSwitchTab = function(btn) {
            var tabId = btn.getAttribute('data-atd-tab');
            document.querySelectorAll('.atd-tab').forEach(function(t) { t.classList.remove('active'); });
            btn.classList.add('active');
            document.querySelectorAll('.atd-panel').forEach(function(p) { p.classList.remove('active'); });
            var target = document.getElementById(tabId);
            if (target) target.classList.add('active');
        };

        // Quick nav from left panel to tab
        window.atdGoTab = function(tabId) {
            var tabBtn = document.querySelector('.atd-tab[data-atd-tab="' + tabId + '"]');
            if (tabBtn) atdSwitchTab(tabBtn);
        };

        // Save consultation
        window.atdSave = function() {
            atdToast('Consulta salva com sucesso');
        };

        // Add prescription item
        window.atdAddRx = function() {
            var nameInput = document.getElementById('atdRxName');
            var name = nameInput ? nameInput.value.trim() : '';
            if (!name) {
                atdToast('Informe o nome do medicamento');
                return;
            }
            var list = document.querySelector('#atd-prescricao .atd-rx-list');
            if (list) {
                var item = document.createElement('div');
                item.className = 'atd-rx-item';
                item.innerHTML = '<span class="atd-rx-icon">💊</span>' +
                    '<div class="atd-rx-body">' +
                    '<div class="atd-rx-name">' + name + '</div>' +
                    '<div class="atd-rx-detail">Configuração pendente</div>' +
                    '</div>' +
                    '<button class="atd-rx-remove" title="Remover" onclick="this.parentElement.remove()">✕</button>';
                list.appendChild(item);
                nameInput.value = '';
                atdToast('Medicamento adicionado');
            }
        };

        // Toast notification
        var toastTimer;
        window.atdToast = function(msg) {
            var toast = document.getElementById('atdToast');
            if (!toast) return;
            clearTimeout(toastTimer);
            toast.textContent = msg;
            toast.classList.add('show');
            toastTimer = setTimeout(function() {
                toast.classList.remove('show');
            }, 2500);
        };

        // Rx remove buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('atd-rx-remove')) {
                e.target.closest('.atd-rx-item').remove();
                atdToast('Item removido');
            }
        });

        // ESC to close
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                var overlay = document.getElementById('atdOverlay');
                if (overlay && overlay.classList.contains('open')) {
                    atdClose();
                }
            }
        });

    })();