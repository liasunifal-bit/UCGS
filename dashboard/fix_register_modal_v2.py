import re

def fix_register_modal():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # --- NEW MODAL HTML (aligned with real profiles schema) ---
    NEW_MODAL = """
<!-- ============================================================
     MODAL DE CADASTRO DE NOVO PROFISSIONAL (v2 — schema real)
     ============================================================ -->
<div id="registerModal" role="dialog" aria-modal="true" aria-labelledby="registerModalTitle"
     style="display:none;position:fixed;inset:0;z-index:10000;background:rgba(11,30,62,0.75);
            backdrop-filter:blur(6px);align-items:center;justify-content:center;padding:20px;">
    <div style="background:#fff;border-radius:16px;width:100%;max-width:580px;
                max-height:93vh;overflow-y:auto;box-shadow:0 24px 64px rgba(0,0,0,0.25);
                animation:modalSlideIn 0.3s ease;">

        <!-- Header -->
        <div style="background:linear-gradient(135deg,#0B1E3E 0%,#1A3A6B 100%);
                    padding:28px 32px 24px;border-radius:16px 16px 0 0;position:relative;">
            <button id="closeRegisterModal" aria-label="Fechar"
                    style="position:absolute;top:16px;right:16px;background:rgba(255,255,255,0.1);
                           border:none;cursor:pointer;border-radius:8px;width:36px;height:36px;
                           display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;">✕</button>
            <p style="margin:0 0 4px;color:#60C4FF;font-size:10px;letter-spacing:2px;text-transform:uppercase;font-weight:600;">NOVO ACESSO</p>
            <h2 id="registerModalTitle" style="margin:0;color:#fff;font-size:20px;font-weight:700;">Cadastro de Profissional</h2>
            <p style="margin:6px 0 0;color:#8BAFD4;font-size:13px;">Preencha seus dados institucionais para acessar o sistema UCGS.</p>
        </div>

        <!-- Body -->
        <div style="padding:28px 32px 32px;">
            <div id="registerAlert" style="display:none;padding:12px 16px;border-radius:8px;margin-bottom:20px;
                 border-left:4px solid;font-size:13px;line-height:1.5;"></div>

            <form id="registerForm" novalidate autocomplete="off">

                <!-- SEÇÃO: Dados Pessoais -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#94A3B8;">Dados Pessoais</p>

                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regNomeCompleto">Nome completo *</label>
                    <input type="text" id="regNomeCompleto" name="nome_completo" required placeholder="Ex.: Dra. Maria da Silva"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                </div>

                <!-- SEÇÃO: Dados Profissionais -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#94A3B8;
                          border-top:1px solid #F1F5F9;padding-top:18px;">Dados Profissionais</p>

                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regRole">Função / Categoria *</label>
                    <select id="regRole" name="role" required
                            style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;background:#fff;transition:border 0.2s;">
                        <option value="">Selecione...</option>
                        <option value="medico">Médico(a)</option>
                        <option value="enfermeiro">Enfermeiro(a)</option>
                        <option value="fisio">Fisioterapeuta</option>
                        <option value="dentista">Dentista</option>
                        <option value="psicologo">Psicólogo(a)</option>
                        <option value="nutricionista">Nutricionista</option>
                        <option value="sesmt">SESMT</option>
                        <option value="admin">Administrador do Sistema</option>
                    </select>
                </div>

                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regEspecialidade">Especialidade</label>
                    <input type="text" id="regEspecialidade" name="especialidade" placeholder="Ex.: Cardiologia, Pediatria, UTI..."
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;">
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regRegistro">Registro Profissional</label>
                        <input type="text" id="regRegistro" name="registro_profissional" placeholder="CRM, COREN, CREFITO..."
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                    </div>
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regMatricula">Matrícula Institucional</label>
                        <input type="text" id="regMatricula" name="matricula" placeholder="Ex.: 2024001"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                    </div>
                </div>

                <div style="margin-bottom:20px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regSetor">Setor / Unidade</label>
                    <input type="text" id="regSetor" name="setor" placeholder="Ex.: UTI Adulto, Ambulatório, SESMT..."
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                </div>

                <!-- SEÇÃO: Dados de Acesso -->
                <p style="margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#94A3B8;
                          border-top:1px solid #F1F5F9;padding-top:18px;">Dados de Acesso</p>

                <div style="margin-bottom:16px;">
                    <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regEmail">E-mail institucional *</label>
                    <input type="email" id="regEmail" name="email" required placeholder="nome@ucgs.edu.br"
                           style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:8px;">
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regSenha">Senha *</label>
                        <input type="password" id="regSenha" name="senha" required minlength="8" placeholder="Mín. 8 caracteres"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                    </div>
                    <div>
                        <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;" for="regConfirmar">Confirmar senha *</label>
                        <input type="password" id="regConfirmar" name="confirmar" required placeholder="Repita a senha"
                               style="width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #D1D5DB;border-radius:8px;font-size:14px;color:#111827;outline:none;transition:border 0.2s;" />
                    </div>
                </div>

                <!-- Password strength -->
                <div id="regStrengthWrap" style="margin-bottom:20px;display:none;">
                    <div style="height:4px;border-radius:4px;background:#E5E7EB;overflow:hidden;margin-bottom:4px;">
                        <div id="regStrengthBar" style="height:100%;width:0%;transition:width 0.3s,background 0.3s;border-radius:4px;"></div>
                    </div>
                    <span id="regStrengthLabel" style="font-size:11px;color:#6B7280;"></span>
                </div>

                <!-- LGPD -->
                <label style="display:flex;gap:10px;align-items:flex-start;margin-bottom:24px;cursor:pointer;font-size:13px;color:#4B5563;line-height:1.5;">
                    <input type="checkbox" id="regLgpd" required style="margin-top:2px;accent-color:#1B6EF5;flex-shrink:0;" />
                    <span>Declaro que li e aceito os
                        <a href="#" style="color:#1B6EF5;text-decoration:none;font-weight:600;">Termos de Uso</a> e a
                        <a href="#" style="color:#1B6EF5;text-decoration:none;font-weight:600;">Política de Privacidade</a>
                        do sistema UCGS, em conformidade com a LGPD.
                    </span>
                </label>

                <button type="submit" id="regSubmitBtn"
                        style="width:100%;padding:14px;background:linear-gradient(135deg,#1B6EF5,#0D50BF);color:#fff;border:none;
                               border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;letter-spacing:0.2px;
                               display:flex;align-items:center;justify-content:center;gap:10px;transition:opacity 0.2s;">
                    <span id="regSubmitLabel">Criar minha conta</span>
                </button>

                <p style="text-align:center;margin:16px 0 0;color:#6B7280;font-size:13px;">
                    Já possui acesso?
                    <button type="button" id="backToLoginBtn"
                            style="background:none;border:none;color:#1B6EF5;font-weight:600;cursor:pointer;font-size:13px;padding:0;">
                        Entrar no sistema
                    </button>
                </p>
            </form>
        </div>
    </div>
</div>

<style>
@keyframes modalSlideIn {
    from { opacity:0; transform:translateY(-20px) scale(0.98); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
#registerModal input:focus, #registerModal select:focus {
    border-color:#1B6EF5 !important;
    box-shadow:0 0 0 3px rgba(27,110,245,0.12);
}
</style>"""

    NEW_SCRIPT = """
    <!-- Register Modal Script v2 -->
    <script>
    (function() {
        var modal     = document.getElementById('registerModal');
        var openBtn   = document.getElementById('registerBtn');
        var closeBtn  = document.getElementById('closeRegisterModal');
        var backBtn   = document.getElementById('backToLoginBtn');
        var form      = document.getElementById('registerForm');
        var submitBtn = document.getElementById('regSubmitBtn');
        var submitLbl = document.getElementById('regSubmitLabel');
        var alertBox  = document.getElementById('registerAlert');

        function showAlert(msg, isSuccess) {
            if (!alertBox) return;
            alertBox.textContent = msg;
            alertBox.style.display = 'block';
            alertBox.style.background  = isSuccess ? '#ECFDF5' : '#FEF2F2';
            alertBox.style.borderColor = isSuccess ? '#10B981' : '#EF4444';
            alertBox.style.color       = isSuccess ? '#065F46' : '#991B1B';
        }

        function openModal() { modal.style.display='flex'; document.getElementById('regNomeCompleto').focus(); }
        function closeModal(){ modal.style.display='none'; }

        if (openBtn)  openBtn.addEventListener('click',  openModal);
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        if (backBtn)  backBtn.addEventListener('click',  closeModal);
        modal.addEventListener('click', function(e){ if(e.target===modal) closeModal(); });
        document.addEventListener('keydown', function(e){ if(e.key==='Escape' && modal.style.display==='flex') closeModal(); });

        // Password strength
        var senhaInput = document.getElementById('regSenha');
        if (senhaInput) {
            senhaInput.addEventListener('input', function() {
                var pw   = this.value;
                var wrap = document.getElementById('regStrengthWrap');
                var bar  = document.getElementById('regStrengthBar');
                var lbl  = document.getElementById('regStrengthLabel');
                if (!pw) { wrap.style.display='none'; return; }
                wrap.style.display='block';
                var s = 0;
                if (pw.length >= 8)       s++;
                if (/[A-Z]/.test(pw))     s++;
                if (/[0-9]/.test(pw))     s++;
                if (/[^A-Za-z0-9]/.test(pw)) s++;
                var lvl = [
                    {p:'25%', c:'#EF4444', t:'Senha fraca'},
                    {p:'50%', c:'#F59E0B', t:'Senha razoável'},
                    {p:'75%', c:'#3B82F6', t:'Senha boa'},
                    {p:'100%',c:'#10B981', t:'Senha forte'},
                ][s-1] || {p:'25%',c:'#EF4444',t:'Senha fraca'};
                bar.style.width=lvl.p; bar.style.background=lvl.c;
                lbl.style.color=lvl.c; lbl.textContent=lvl.t;
            });
        }

        if (form) {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();

                var nomeCompleto         = (document.getElementById('regNomeCompleto')?.value || '').trim();
                var role                 = document.getElementById('regRole')?.value || '';
                var especialidade        = (document.getElementById('regEspecialidade')?.value || '').trim();
                var registro_profissional= (document.getElementById('regRegistro')?.value || '').trim();
                var matricula            = (document.getElementById('regMatricula')?.value || '').trim();
                var setor                = (document.getElementById('regSetor')?.value || '').trim();
                var email                = (document.getElementById('regEmail')?.value || '').trim();
                var senha                = document.getElementById('regSenha')?.value || '';
                var confirmar            = document.getElementById('regConfirmar')?.value || '';
                var lgpd                 = document.getElementById('regLgpd')?.checked;

                if (!nomeCompleto || !role || !email || !senha || !confirmar) {
                    showAlert('Preencha todos os campos obrigatórios (*).', false); return;
                }
                if (senha.length < 8) {
                    showAlert('A senha deve ter no mínimo 8 caracteres.', false); return;
                }
                if (senha !== confirmar) {
                    showAlert('As senhas não coincidem. Verifique e tente novamente.', false); return;
                }
                if (!lgpd) {
                    showAlert('Você precisa aceitar os Termos de Uso para continuar.', false); return;
                }

                var client = window._supa;
                if (!client) {
                    showAlert('Conexão com o servidor não estabelecida. Aguarde e tente novamente.', false); return;
                }

                submitBtn.disabled = true;
                submitLbl.textContent = 'Criando conta...';

                try {
                    var r = await client.auth.signUp({
                        email: email,
                        password: senha,
                        options: {
                            data: {
                                nome_completo:          nomeCompleto,
                                role:                   role,
                                especialidade:          especialidade,
                                registro_profissional:  registro_profissional,
                                matricula:              matricula,
                                setor:                  setor
                            }
                        }
                    });

                    if (r.error) throw r.error;

                    showAlert('Conta criada com sucesso! Você já pode fazer login.', true);
                    submitLbl.textContent = 'Conta criada!';

                    setTimeout(function() {
                        closeModal();
                        var loginInput = document.getElementById('userInput');
                        if (loginInput) loginInput.value = email;
                        var passInput = document.getElementById('passwordInput');
                        if (passInput) passInput.focus();
                    }, 2500);

                } catch(err) {
                    console.error('[UCGS] Erro no registro:', err);
                    var msg = err.message || 'Não foi possível criar a conta.';
                    if (msg.includes('already registered')) msg = 'Este e-mail já está cadastrado. Use a opção "Entrar no sistema".';
                    if (msg.includes('Password'))          msg = 'Senha muito fraca. Use letras maiúsculas, números e símbolos.';
                    showAlert(msg, false);
                    submitBtn.disabled = false;
                    submitLbl.textContent = 'Criar minha conta';
                }
            });
        }
    })();
    </script>"""

    # Remove old modal HTML (between the comment and the closing </div> of the modal)
    html = re.sub(
        r'<!-- ={10,}.*?MODAL DE CADASTRO.*?</div>\s*<!-- Register Modal Script -->.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    # Also remove the v2 comment pattern if it exists
    html = re.sub(
        r'<!-- ={10,}.*?MODAL DE CADASTRO.*?</style>',
        '',
        html,
        flags=re.DOTALL
    )

    # Remove old register scripts
    html = re.sub(
        r'<!-- Register Modal Script(?:\s*v\d+)? -->.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    # Inject new modal + script before </body>
    html = html.replace('</body>', NEW_MODAL + '\n' + NEW_SCRIPT + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Modal de cadastro atualizado para o schema real!')

    # Verify
    with open(path, 'r', encoding='utf-8') as f:
        check = f.read()

    fields = {
        'regNomeCompleto': 'Campo nome_completo',
        'regRole': 'Select role',
        'regEspecialidade': 'Campo especialidade',
        'regRegistro': 'Campo registro_profissional',
        'regMatricula': 'Campo matricula',
        'regSetor': 'Campo setor',
        'registro_profissional': 'Metadado registro_profissional no signUp',
        'nome_completo': 'Metadado nome_completo no signUp',
        'regStrengthBar': 'Indicador de forca da senha',
    }
    for key, label in fields.items():
        print(label + ': ' + ('OK' if key in check else 'AUSENTE'))

if __name__ == '__main__':
    fix_register_modal()
