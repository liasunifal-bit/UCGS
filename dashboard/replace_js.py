import re

def main():
    index_path = r"c:\Users\maria\Downloads\antigravity lias\dashboard\index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_script = """<script type="module">
    import { AuthService } from './js/auth/auth-service.js';

    const authOverlay  = document.getElementById('authOverlay');
    const emailInput   = document.getElementById('authEmail');
    const passInput    = document.getElementById('authPass');
    const submitBtn    = document.getElementById('authBtn');
    const alertBox     = document.getElementById('authAlertBox');
    const alertTitle   = document.getElementById('authAlertTitle');
    const alertMsg     = document.getElementById('authAlertMsg');
    const togglePwd    = document.getElementById('authTogglePwd');
    const eyeIcon      = document.getElementById('authEyeIcon');

    const MESSAGES = {
        INVALID:     { title: 'Credenciais inseridas incorretas.',           msg: 'Verifique seu usuário e senha e tente novamente.' },
        BLOCKED:     { title: 'Acesso negado pelo administrador.',           msg: 'Entre em contato com o setor responsável para regularização.' },
        UNAVAILABLE: { title: 'Serviço indisponível no momento.',            msg: 'Tente novamente em instantes ou acione a Central de Suporte.' },
        EMPTY:       { title: 'Campos obrigatórios.',                        msg: 'Informe usuário e senha para continuar.' },
    };

    function showAlert(key) {
        const m = MESSAGES[key] || MESSAGES.INVALID;
        alertTitle.textContent = m.title;
        alertMsg.textContent   = m.msg;
        alertBox.classList.add('visible');
    }

    function hideAlert() { alertBox.classList.remove('visible'); }

    // Toggle mostrar/ocultar senha
    togglePwd.addEventListener('click', () => {
        const visible = passInput.type === 'text';
        passInput.type = visible ? 'password' : 'text';
        togglePwd.setAttribute('aria-label', visible ? 'Mostrar senha' : 'Ocultar senha');
        eyeIcon.innerHTML = visible
            ? '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>'
            : '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
    });

    // Limpar erros ao digitar
    [emailInput, passInput].forEach(el => {
        el.addEventListener('input', () => {
            el.classList.remove('has-error');
            hideAlert();
        });
    });

    // Verificar sessão existente
    document.addEventListener('DOMContentLoaded', async () => {
        document.body.style.overflow = 'hidden';
        try {
            const session = await AuthService.getSession();
            if (session) {
                authOverlay.style.display = 'none';
                document.body.style.overflow = '';
            }
        } catch(e) {}
        emailInput.focus();
    });

    // Login via Supabase JWT
    submitBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        const pass  = passInput.value;

        if (!email || !pass) {
            if (!email) emailInput.classList.add('has-error');
            if (!pass)  passInput.classList.add('has-error');
            showAlert('EMPTY');
            return;
        }

        hideAlert();
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        try {
            await AuthService.login(email, pass);
            submitBtn.querySelector('.auth-btn-label').textContent = 'Redirecionando…';
            authOverlay.style.display = 'none';
            document.body.style.overflow = '';
        } catch (error) {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            emailInput.classList.add('has-error');
            passInput.classList.add('has-error');
            passInput.focus();
            showAlert(error.message.includes('blocked') ? 'BLOCKED' : 'INVALID');
        }
    });
</script>"""

    new_script = """<script type="module">
    import { AuthService } from './js/auth/auth-service.js';

    const authOverlay  = document.getElementById('authOverlay');
    const emailInput   = document.getElementById('userInput');
    const passInput    = document.getElementById('passwordInput');
    const submitBtn    = document.getElementById('submitBtn');
    const alertBox     = document.getElementById('formAlert');
    const alertTitle   = document.getElementById('formAlertTitle');
    const alertMsg     = document.getElementById('formAlertMsg');
    const togglePwd    = document.getElementById('togglePassword');
    const eyeIcon      = document.getElementById('eyeIcon');
    const googleBtn    = document.getElementById('googleBtn');

    const MESSAGES = {
        INVALID:     { title: 'Credenciais inseridas incorretas.',           msg: 'Verifique seu usuário e senha e tente novamente.' },
        BLOCKED:     { title: 'Acesso negado pelo administrador.',           msg: 'Entre em contato com o setor responsável para regularização.' },
        UNAVAILABLE: { title: 'Serviço indisponível no momento.',            msg: 'Tente novamente em instantes ou acione a Central de Suporte.' },
        EMPTY:       { title: 'Campos obrigatórios.',                        msg: 'Informe usuário e senha para continuar.' },
    };

    function showAlert(key) {
        const m = MESSAGES[key] || MESSAGES.INVALID;
        alertTitle.textContent = m.title;
        alertMsg.textContent   = m.msg;
        alertBox.classList.add('visible');
    }

    function hideAlert() { alertBox.classList.remove('visible'); }

    // Toggle mostrar/ocultar senha
    if (togglePwd && passInput) {
        togglePwd.addEventListener('click', () => {
            const visible = passInput.type === 'text';
            passInput.type = visible ? 'password' : 'text';
            togglePwd.setAttribute('aria-label', visible ? 'Mostrar senha' : 'Ocultar senha');
            if (eyeIcon) {
                eyeIcon.innerHTML = visible
                    ? '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>'
                    : '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
            }
        });
    }

    // Limpar erros ao digitar
    [emailInput, passInput].forEach(el => {
        if (el) {
            el.addEventListener('input', () => {
                el.classList.remove('has-error');
                hideAlert();
            });
        }
    });

    // Verificar sessão existente
    document.addEventListener('DOMContentLoaded', async () => {
        document.body.style.overflow = 'hidden';
        try {
            const session = await AuthService.getSession();
            if (session) {
                if (authOverlay) authOverlay.style.display = 'none';
                document.body.style.overflow = '';
            }
        } catch(e) {}
        if (emailInput) emailInput.focus();
    });

    // Login via Supabase JWT
    if (submitBtn) {
        submitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const email = emailInput.value.trim();
            const pass  = passInput.value;

            if (!email || !pass) {
                if (!email) emailInput.classList.add('has-error');
                if (!pass)  passInput.classList.add('has-error');
                showAlert('EMPTY');
                return;
            }

            hideAlert();
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;

            try {
                await AuthService.login(email, pass);
                const label = submitBtn.querySelector('.form-submit-label');
                if (label) label.textContent = 'Redirecionando…';
                if (authOverlay) authOverlay.style.display = 'none';
                document.body.style.overflow = '';
            } catch (error) {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
                emailInput.classList.add('has-error');
                passInput.classList.add('has-error');
                passInput.focus();
                showAlert(error.message.includes('blocked') ? 'BLOCKED' : 'INVALID');
            }
        });
    }

    // Login via Google SSO
    if (googleBtn) {
        googleBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                googleBtn.classList.add('loading');
                await AuthService.signInWithOAuth('google');
            } catch (error) {
                googleBtn.classList.remove('loading');
                showAlert('UNAVAILABLE');
            }
        });
    }
</script>"""

    content = content.replace(old_script, new_script)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Script replaced.")

if __name__ == "__main__":
    main()
