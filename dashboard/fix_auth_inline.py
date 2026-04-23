import re

def fix_auth_integration():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix registerBtn styling - ensure it has visible blue styling
    html = html.replace(
        '<button type="button" class="form-submit" id="registerBtn" style="background: var(--brand-blue); margin-top: 10px;">',
        '<button type="button" class="form-submit" id="registerBtn" style="background: #1a56db; margin-top: 10px; color: white;">'
    )

    # 2. Inject inline auth handler right before </body> that uses the already-loaded supabase client
    auth_script = """
    <!-- Auth Integration Inline Script -->
    <script>
    (function() {
        // Wait for DOM + Supabase to be ready
        function initAuthHandlers() {
            var submitBtn = document.getElementById('submitBtn');
            var registerBtn = document.getElementById('registerBtn');
            var userInput = document.getElementById('userInput');
            var passInput = document.getElementById('passwordInput');
            var alertBox = document.getElementById('formAlert');
            var alertTitle = document.getElementById('formAlertTitle');
            var alertMsg = document.getElementById('formAlertMsg');

            function showAlert(title, msg, isSuccess) {
                if (!alertBox) return;
                if (alertTitle) alertTitle.textContent = title;
                if (alertMsg) alertMsg.textContent = msg;
                alertBox.classList.add('visible');
                alertBox.style.borderColor = isSuccess ? '#10B981' : '#EF4444';
                alertBox.style.background = isSuccess ? '#ECFDF5' : '';
            }

            function getClient() {
                // Find supabase client from window
                if (window._supabaseClient) return window._supabaseClient;
                return null;
            }

            function removeOverlay() {
                var overlay = document.getElementById('authOverlay');
                if (overlay) {
                    overlay.style.transition = 'opacity 0.5s';
                    overlay.style.opacity = '0';
                    setTimeout(function() { overlay.style.display = 'none'; }, 500);
                }
            }

            function setLoading(loading) {
                if (submitBtn) submitBtn.disabled = loading;
                if (registerBtn) registerBtn.disabled = loading;
                if (userInput) userInput.disabled = loading;
                if (passInput) passInput.disabled = loading;
            }

            if (submitBtn) {
                submitBtn.addEventListener('click', async function(e) {
                    e.preventDefault();
                    var email = userInput ? userInput.value.trim() : '';
                    var pass = passInput ? passInput.value : '';
                    if (!email || !pass) {
                        showAlert('Campos obrigatórios.', 'Informe e-mail e senha para continuar.', false);
                        return;
                    }
                    setLoading(true);
                    try {
                        var client = getClient();
                        if (client) {
                            var result = await client.auth.signInWithPassword({ email: email, password: pass });
                            if (result.error) throw result.error;
                            showAlert('Login realizado!', 'Autenticado com sucesso. Carregando painel...', true);
                            setTimeout(removeOverlay, 1000);
                        } else {
                            showAlert('Erro de configuração', 'Cliente Supabase não encontrado.', false);
                        }
                    } catch(err) {
                        showAlert('Erro ao entrar.', err.message || 'Credenciais inválidas.', false);
                    } finally {
                        setLoading(false);
                    }
                });
            }

            if (registerBtn) {
                registerBtn.addEventListener('click', async function() {
                    var email = userInput ? userInput.value.trim() : '';
                    var pass = passInput ? passInput.value : '';
                    if (!email || !pass) {
                        showAlert('Campos obrigatórios.', 'Informe e-mail e senha para registrar.', false);
                        return;
                    }
                    if (pass.length < 6) {
                        showAlert('Senha muito curta.', 'A senha deve ter pelo menos 6 caracteres.', false);
                        return;
                    }
                    setLoading(true);
                    registerBtn.textContent = 'Registrando...';
                    try {
                        var client = getClient();
                        if (client) {
                            var result = await client.auth.signUp({ email: email, password: pass });
                            if (result.error) throw result.error;
                            showAlert('Conta criada!', 'Registro concluído. Entrando no sistema...', true);
                            // Auto-login after registration
                            setTimeout(async function() {
                                try {
                                    var loginResult = await client.auth.signInWithPassword({ email: email, password: pass });
                                    if (!loginResult.error) removeOverlay();
                                } catch(e) {}
                            }, 1500);
                        } else {
                            showAlert('Erro de configuração', 'Cliente Supabase não encontrado.', false);
                        }
                    } catch(err) {
                        showAlert('Erro ao registrar.', err.message || 'Não foi possível criar a conta.', false);
                    } finally {
                        setLoading(false);
                        registerBtn.textContent = 'Registrar Nova Conta';
                    }
                });
            }
        }

        // Run after page loads
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initAuthHandlers);
        } else {
            initAuthHandlers();
        }
    })();
    </script>
"""

    # Remove old login-ui.js script tag if present (to avoid double listeners)
    html = re.sub(r'\s*<script src="js/modules/login-ui\.js"></script>', '', html)

    # Inject before </body>
    if '<!-- Auth Integration Inline Script -->' not in html:
        html = html.replace('</body>', auth_script + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Auth integration fixed in index.html!")

if __name__ == '__main__':
    fix_auth_integration()
