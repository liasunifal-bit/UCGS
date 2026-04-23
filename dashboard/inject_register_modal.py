import re

REGISTER_MODAL_HTML = """
<!-- ============================================================
     MODAL DE CADASTRO DE NOVO PROFISSIONAL
     ============================================================ -->
<div id="registerModal" role="dialog" aria-modal="true" aria-labelledby="registerModalTitle"
     style="display:none;position:fixed;inset:0;z-index:10000;background:rgba(11,30,62,0.7);
            backdrop-filter:blur(6px);align-items:center;justify-content:center;padding:20px;">
    <div style="background:#fff;border-radius:16px;width:100%;max-width:560px;
                max-height:92vh;overflow-y:auto;box-shadow:0 24px 64px rgba(0,0,0,0.22);
                animation:modalSlideIn 0.3s ease;">

        <!-- Modal Header -->
        <div style="background:linear-gradient(135deg,#0B1E3E 0%,#1A3A6B 100%);
                    padding:28px 32px 24px;border-radius:16px 16px 0 0;position:relative;">
            <button id="closeRegisterModal" aria-label="Fechar"
                    style="position:absolute;top:16px;right:16px;background:rgba(255,255,255,0.1);
                           border:none;cursor:pointer;border-radius:8px;width:36px;height:36px;
                           display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;">
                ✕
            </button>
            <p style="margin:0 0 4px;color:#60C4FF;font-size:10px;letter-spacing:2px;
                      text-transform:uppercase;font-weight:600;">NOVO ACESSO</p>
            <h2 id="registerModalTitle" style="margin:0;color:#fff;font-size:20px;font-weight:700;">
                Cadastro de Profissional
            </h2>
            <p style="margin:6px 0 0;color:#8BAFD4;font-size:13px;">
                Preencha seus dados institucionais para solicitar acesso ao sistema UCGS.
            </p>
        </div>

        <!-- Modal Body -->
        <div style="padding:28px 32px 32px;">

            <!-- Alert box -->
            <div id="registerAlert" style="display:none;padding:12px 16px;border-radius:8px;
                 margin-bottom:20px;border-left:4px solid;font-size:13px;line-height:1.5;"></div>

            <!-- Form -->
            <form id="registerForm" novalidate autocomplete="off">
                <!-- Section: Dados Pessoais -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;
                          text-transform:uppercase;color:#94A3B8;">Dados Pessoais</p>

                <!-- Nome completo -->
                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                  margin-bottom:6px;" for="regNome">Nome completo *</label>
                    <input type="text" id="regNome" name="nome" required
                           placeholder="Ex.: Dra. Maria da Silva"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                  border-radius:8px;font-size:14px;color:#111827;outline:none;
                                  transition:border 0.2s;" />
                </div>

                <!-- CPF -->
                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                  margin-bottom:6px;" for="regCPF">CPF *</label>
                    <input type="text" id="regCPF" name="cpf" required
                           placeholder="000.000.000-00" maxlength="14"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                  border-radius:8px;font-size:14px;color:#111827;outline:none;
                                  transition:border 0.2s;" />
                </div>

                <!-- Telefone -->
                <div style="margin-bottom:20px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                  margin-bottom:6px;" for="regTelefone">Telefone</label>
                    <input type="tel" id="regTelefone" name="telefone"
                           placeholder="(00) 90000-0000"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                  border-radius:8px;font-size:14px;color:#111827;outline:none;
                                  transition:border 0.2s;" />
                </div>

                <!-- Section: Dados Profissionais -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;
                          text-transform:uppercase;color:#94A3B8;border-top:1px solid #F1F5F9;padding-top:18px;">
                    Dados Profissionais</p>

                <!-- Categoria profissional -->
                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                  margin-bottom:6px;" for="regCategoria">Categoria profissional *</label>
                    <select id="regCategoria" name="categoria" required
                            style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                   border-radius:8px;font-size:14px;color:#111827;outline:none;background:#fff;
                                   transition:border 0.2s;">
                        <option value="">Selecione...</option>
                        <option value="medico">Médico(a)</option>
                        <option value="enfermeiro">Enfermeiro(a)</option>
                        <option value="fisioterapeuta">Fisioterapeuta</option>
                        <option value="dentista">Dentista</option>
                        <option value="psicologo">Psicólogo(a)</option>
                        <option value="nutricionista">Nutricionista</option>
                        <option value="farmaceutico">Farmacêutico(a)</option>
                        <option value="assistente_social">Assistente Social</option>
                        <option value="administrativo">Administrativo</option>
                        <option value="admin">Administrador do Sistema</option>
                    </select>
                </div>

                <!-- Número de registro + Setor (side by side) -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;">
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                      margin-bottom:6px;" for="regNumRegistro">Nº Registro (CRM/COREN…)</label>
                        <input type="text" id="regNumRegistro" name="num_registro"
                               placeholder="Ex.: CRM-SP 12345"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                      border-radius:8px;font-size:14px;color:#111827;outline:none;
                                      transition:border 0.2s;" />
                    </div>
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                      margin-bottom:6px;" for="regSetor">Setor / Unidade</label>
                        <input type="text" id="regSetor" name="setor"
                               placeholder="Ex.: UTI Adulto"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                      border-radius:8px;font-size:14px;color:#111827;outline:none;
                                      transition:border 0.2s;" />
                    </div>
                </div>

                <!-- Section: Acesso -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;
                          text-transform:uppercase;color:#94A3B8;border-top:1px solid #F1F5F9;padding-top:18px;">
                    Dados de Acesso</p>

                <!-- E-mail -->
                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                  margin-bottom:6px;" for="regEmail">E-mail institucional *</label>
                    <input type="email" id="regEmail" name="email" required
                           placeholder="nome@ucgs.edu.br"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                  border-radius:8px;font-size:14px;color:#111827;outline:none;
                                  transition:border 0.2s;" />
                </div>

                <!-- Senha + Confirmar (side by side) -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px;">
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                      margin-bottom:6px;" for="regSenha">Senha *</label>
                        <input type="password" id="regSenha" name="senha" required minlength="8"
                               placeholder="Mín. 8 caracteres"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                      border-radius:8px;font-size:14px;color:#111827;outline:none;
                                      transition:border 0.2s;" />
                    </div>
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;
                                      margin-bottom:6px;" for="regConfirmarSenha">Confirmar senha *</label>
                        <input type="password" id="regConfirmarSenha" name="confirmar_senha" required
                               placeholder="Repita a senha"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;
                                      border-radius:8px;font-size:14px;color:#111827;outline:none;
                                      transition:border 0.2s;" />
                    </div>
                </div>

                <!-- Strength indicator -->
                <div id="regPasswordStrength" style="margin-top:-16px;margin-bottom:20px;display:none;">
                    <div style="height:4px;border-radius:4px;background:#E5E7EB;overflow:hidden;margin-bottom:4px;">
                        <div id="regStrengthBar" style="height:100%;width:0%;transition:width 0.3s,background 0.3s;border-radius:4px;"></div>
                    </div>
                    <span id="regStrengthLabel" style="font-size:11px;color:#6B7280;"></span>
                </div>

                <!-- LGPD Consent -->
                <label style="display:flex;gap:10px;align-items:flex-start;margin-bottom:24px;
                              cursor:pointer;font-size:13px;color:#4B5563;line-height:1.5;">
                    <input type="checkbox" id="regLgpd" required
                           style="margin-top:2px;accent-color:#1B6EF5;flex-shrink:0;" />
                    <span>
                        Declaro que li e aceito os
                        <a href="#" style="color:#1B6EF5;text-decoration:none;font-weight:600;">Termos de Uso</a>
                        e a
                        <a href="#" style="color:#1B6EF5;text-decoration:none;font-weight:600;">Política de Privacidade</a>
                        do sistema UCGS, em conformidade com a LGPD.
                    </span>
                </label>

                <!-- Submit button -->
                <button type="submit" id="regSubmitBtn"
                        style="width:100%;padding:14px;background:linear-gradient(135deg,#1B6EF5,#0D50BF);
                               color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;
                               cursor:pointer;letter-spacing:0.2px;display:flex;align-items:center;
                               justify-content:center;gap:10px;transition:opacity 0.2s;">
                    <span id="regSubmitLabel">Criar minha conta</span>
                </button>

                <p style="text-align:center;margin:16px 0 0;color:#6B7280;font-size:13px;">
                    Já possui acesso?
                    <button type="button" id="backToLoginBtn"
                            style="background:none;border:none;color:#1B6EF5;font-weight:600;
                                   cursor:pointer;font-size:13px;padding:0;">
                        Entrar no sistema
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>

<style>
@keyframes modalSlideIn {
    from { opacity: 0; transform: translateY(-20px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}
#registerModal input:focus,
#registerModal select:focus {
    border-color: #1B6EF5 !important;
    box-shadow: 0 0 0 3px rgba(27,110,245,0.12);
}
</style>
"""

REGISTER_MODAL_SCRIPT = """
    <!-- Register Modal Script -->
    <script>
    (function() {
        var modal     = document.getElementById('registerModal');
        var openBtn   = document.getElementById('registerBtn');
        var closeBtn  = document.getElementById('closeRegisterModal');
        var backBtn   = document.getElementById('backToLoginBtn');
        var form      = document.getElementById('registerForm');
        var submitBtn = document.getElementById('regSubmitBtn');
        var submitLbl = document.getElementById('regSubmitLabel');
        var alert     = document.getElementById('registerAlert');

        // CPF mask
        document.getElementById('regCPF').addEventListener('input', function(e) {
            var v = e.target.value.replace(/\\D/g,'').slice(0,11);
            if (v.length > 9)      v = v.slice(0,3)+'.'+v.slice(3,6)+'.'+v.slice(6,9)+'-'+v.slice(9);
            else if (v.length > 6) v = v.slice(0,3)+'.'+v.slice(3,6)+'.'+v.slice(6);
            else if (v.length > 3) v = v.slice(0,3)+'.'+v.slice(3);
            e.target.value = v;
        });

        // Phone mask
        document.getElementById('regTelefone').addEventListener('input', function(e) {
            var v = e.target.value.replace(/\\D/g,'').slice(0,11);
            if (v.length > 6) v = '('+v.slice(0,2)+') '+v.slice(2,7)+'-'+v.slice(7);
            else if (v.length > 2) v = '('+v.slice(0,2)+') '+v.slice(2);
            e.target.value = v;
        });

        // Password strength
        document.getElementById('regSenha').addEventListener('input', function() {
            var pw   = this.value;
            var bar  = document.getElementById('regStrengthBar');
            var lbl  = document.getElementById('regStrengthLabel');
            var wrap = document.getElementById('regPasswordStrength');
            if (!pw) { wrap.style.display='none'; return; }
            wrap.style.display = 'block';
            var score = 0;
            if (pw.length >= 8)  score++;
            if (/[A-Z]/.test(pw)) score++;
            if (/[0-9]/.test(pw)) score++;
            if (/[^A-Za-z0-9]/.test(pw)) score++;
            var levels = [
                {pct:'25%',  color:'#EF4444', txt:'Senha fraca'},
                {pct:'50%',  color:'#F59E0B', txt:'Senha razoável'},
                {pct:'75%',  color:'#3B82F6', txt:'Senha boa'},
                {pct:'100%', color:'#10B981', txt:'Senha forte'},
            ];
            var l = levels[score-1] || levels[0];
            bar.style.width      = l.pct;
            bar.style.background = l.color;
            lbl.style.color      = l.color;
            lbl.textContent      = l.txt;
        });

        function showAlert(msg, isSuccess) {
            if (!alert) return;
            alert.textContent = msg;
            alert.style.display = 'block';
            alert.style.background   = isSuccess ? '#ECFDF5' : '#FEF2F2';
            alert.style.borderColor  = isSuccess ? '#10B981'  : '#EF4444';
            alert.style.color        = isSuccess ? '#065F46'  : '#991B1B';
        }

        function openModal() {
            modal.style.display = 'flex';
            document.getElementById('regNome').focus();
        }
        function closeModal() { modal.style.display = 'none'; }

        if (openBtn) openBtn.addEventListener('click', openModal);
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        if (backBtn)  backBtn.addEventListener('click',  closeModal);
        modal.addEventListener('click', function(e){ if(e.target===modal) closeModal(); });

        // Keyboard ESC
        document.addEventListener('keydown', function(e){
            if (e.key==='Escape' && modal.style.display==='flex') closeModal();
        });

        if (form) {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                var nome        = document.getElementById('regNome').value.trim();
                var cpf         = document.getElementById('regCPF').value.trim();
                var telefone    = document.getElementById('regTelefone').value.trim();
                var categoria   = document.getElementById('regCategoria').value;
                var numRegistro = document.getElementById('regNumRegistro').value.trim();
                var setor       = document.getElementById('regSetor').value.trim();
                var email       = document.getElementById('regEmail').value.trim();
                var senha       = document.getElementById('regSenha').value;
                var confirmar   = document.getElementById('regConfirmarSenha').value;
                var lgpd        = document.getElementById('regLgpd').checked;

                // Validação
                if (!nome || !cpf || !categoria || !email || !senha || !confirmar) {
                    showAlert('⚠ Preencha todos os campos obrigatórios (*).', false); return;
                }
                if (cpf.replace(/\\D/g,'').length !== 11) {
                    showAlert('⚠ CPF inválido. Verifique o número informado.', false); return;
                }
                if (senha.length < 8) {
                    showAlert('⚠ A senha deve ter no mínimo 8 caracteres.', false); return;
                }
                if (senha !== confirmar) {
                    showAlert('⚠ As senhas não coincidem. Verifique e tente novamente.', false); return;
                }
                if (!lgpd) {
                    showAlert('⚠ Você precisa aceitar os Termos de Uso para continuar.', false); return;
                }

                submitBtn.disabled = true;
                submitLbl.textContent = 'Criando conta...';

                try {
                    var client = window._supa;
                    if (!client) throw new Error('Cliente Supabase não inicializado.');

                    // 1. Criar usuário no Supabase Auth com metadados
                    var r = await client.auth.signUp({
                        email: email,
                        password: senha,
                        options: {
                            data: {
                                nome:         nome,
                                cpf:          cpf,
                                telefone:     telefone,
                                categoria:    categoria,
                                num_registro: numRegistro,
                                setor:        setor
                            }
                        }
                    });

                    if (r.error) throw r.error;

                    showAlert('✓ Conta criada! Verifique seu e-mail institucional para confirmar o acesso.', true);
                    submitLbl.textContent = 'Conta criada!';

                    setTimeout(function() {
                        closeModal();
                        // Pre-fill login email
                        var loginInput = document.getElementById('userInput');
                        if (loginInput) loginInput.value = email;
                    }, 3000);

                } catch(err) {
                    console.error('Erro no registro:', err);
                    var msg = err.message || 'Não foi possível criar a conta.';
                    if (msg.includes('already registered')) msg = 'Este e-mail já está cadastrado. Faça login.';
                    showAlert('✕ ' + msg, false);
                    submitBtn.disabled   = false;
                    submitLbl.textContent = 'Criar minha conta';
                }
            });
        }
    })();
    </script>
"""

def main():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the "Registrar Nova Conta" button to look like a link (not primary)
    html = re.sub(
        r'<button type="button" class="form-submit" id="registerBtn"[^>]*>.*?</button>',
        '''<button type="button" id="registerBtn"
                        style="width:100%;padding:11px;margin-top:8px;background:transparent;
                               color:#1B6EF5;border:1.5px solid #1B6EF5;border-radius:8px;
                               font-size:14px;font-weight:600;cursor:pointer;transition:all 0.2s;">
                        Não tem conta? Cadastre-se
                    </button>''',
        html,
        flags=re.DOTALL
    )

    # 2. Insert modal HTML before </body>
    if 'id="registerModal"' not in html:
        html = html.replace('</body>', REGISTER_MODAL_HTML + '\n</body>')

    # 3. Insert modal script before </body>
    if 'Register Modal Script' not in html:
        html = html.replace('</body>', REGISTER_MODAL_SCRIPT + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Modal de cadastro inserido com sucesso!")

if __name__ == '__main__':
    main()
