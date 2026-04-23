/* ==========================================================
   UCGS LOGIN — Integração com Supabase
   ========================================================== */
(function () {
    const form        = document.getElementById('loginForm');
    const userInput   = document.getElementById('userInput');
    const passInput   = document.getElementById('passwordInput');
    const toggleBtn   = document.getElementById('togglePassword');
    const eyeIcon     = document.getElementById('eyeIcon');
    const submitBtn   = document.getElementById('submitBtn');
    const registerBtn = document.getElementById('registerBtn');
    const alertBox    = document.getElementById('formAlert');
    const alertTitle  = document.getElementById('formAlertTitle');
    const alertMsg    = document.getElementById('formAlertMsg');

    /* Mensagens profissionais */
    const MESSAGES = {
        EMPTY:        { title: 'Campos obrigatórios.',            msg: 'Informe usuário e senha para continuar.' },
        INVALID:      { title: 'Credenciais incorretas.',         msg: 'Verifique os dados informados e tente novamente.' },
        REGISTER_OK:  { title: 'Registro concluído!',             msg: 'Conta criada com sucesso. Autenticando...' },
        REGISTER_ERR: { title: 'Erro ao registrar.',              msg: 'Não foi possível criar a conta. Verifique os dados.' },
        GENERIC_ERR:  { title: 'Erro de autenticação.',           msg: 'Ocorreu um erro. Tente novamente em instantes.' }
    };

    /* ---------- Mostrar / ocultar senha ---------- */
    if (toggleBtn && passInput) {
        toggleBtn.addEventListener('click', () => {
            const visible = passInput.type === 'text';
            passInput.type = visible ? 'password' : 'text';
            toggleBtn.setAttribute('aria-pressed', String(!visible));
            toggleBtn.setAttribute('aria-label', visible ? 'Mostrar senha' : 'Ocultar senha');
            if (eyeIcon) {
                eyeIcon.innerHTML = visible
                    ? '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>'
                    : '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
            }
        });
    }

    /* ---------- Limpar estado de erro ao digitar ---------- */
    [userInput, passInput].forEach(el => {
        if (el) {
            el.addEventListener('input', () => {
                el.classList.remove('has-error');
                if (alertBox) alertBox.classList.remove('visible');
            });
        }
    });

    /* ---------- Exibir alerta ---------- */
    function showAlert(key, customMsg) {
        if (!alertBox) return;
        const m = MESSAGES[key] || MESSAGES.GENERIC_ERR;
        if (alertTitle) alertTitle.textContent = m.title;
        if (alertMsg) alertMsg.textContent = customMsg || m.msg;
        alertBox.classList.add('visible');
    }

    /* ---------- Helper UI ---------- */
    function setFormLoading(isLoading) {
        if (submitBtn) {
            if (isLoading) submitBtn.classList.add('loading');
            else submitBtn.classList.remove('loading');
            submitBtn.disabled = isLoading;
        }
        if (registerBtn) registerBtn.disabled = isLoading;
        if (userInput) userInput.disabled = isLoading;
        if (passInput) passInput.disabled = isLoading;
    }

    function checkInputs() {
        const user = userInput ? userInput.value.trim() : '';
        const pass = passInput ? passInput.value : '';
        if (!user || !pass) {
            if (!user && userInput) userInput.classList.add('has-error');
            if (!pass && passInput) passInput.classList.add('has-error');
            showAlert('EMPTY');
            if (userInput && passInput) (user ? passInput : userInput).focus();
            return null;
        }
        return { user, pass };
    }

    function removeLoginOverlay() {
        const overlay = document.querySelector('.login-shell');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => { overlay.style.display = 'none'; }, 500);
        }
    }

    /* ---------- Submissão (Login) ---------- */
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputs = checkInputs();
            if (!inputs) return;

            setFormLoading(true);
            try {
                if (window.AuthService) {
                    await window.AuthService.login(inputs.user, inputs.pass);
                    // Login com sucesso
                    if (submitBtn) submitBtn.querySelector('.form-submit-label').textContent = 'Redirecionando...';
                    setTimeout(() => {
                        removeLoginOverlay();
                    }, 500);
                } else {
                    console.error("AuthService não carregado");
                }
            } catch (err) {
                console.error("Erro no login:", err);
                showAlert('INVALID', err.message);
                if (passInput) {
                    passInput.classList.add('has-error');
                    passInput.focus();
                    passInput.select();
                }
            } finally {
                setFormLoading(false);
            }
        });
    }

    /* ---------- Submissão (Registro) ---------- */
    if (registerBtn) {
        registerBtn.addEventListener('click', async () => {
            const inputs = checkInputs();
            if (!inputs) return;

            setFormLoading(true);
            if (registerBtn) registerBtn.textContent = 'Registrando...';
            
            try {
                if (window.AuthService) {
                    await window.AuthService.register(inputs.user, inputs.pass);
                    showAlert('REGISTER_OK');
                    // Logo após registrar, tentar fazer login
                    await window.AuthService.login(inputs.user, inputs.pass);
                    setTimeout(() => {
                        removeLoginOverlay();
                    }, 500);
                }
            } catch (err) {
                console.error("Erro no registro:", err);
                showAlert('REGISTER_ERR', err.message);
            } finally {
                setFormLoading(false);
                if (registerBtn) registerBtn.textContent = 'Registrar Nova Conta';
            }
        });
    }

    /* ---------- UX: foco inicial ---------- */
    window.addEventListener('load', () => {
        if (userInput) userInput.focus();
    });

})();