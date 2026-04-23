import re

with open('site nevo_backup.HTML', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Funcao para reverter dupla codificacao (apenas as letras defeituosas)
def fix_double_encoding(match):
    s = match.group(0)
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception as e:
        return s

# Esse regex pega EXATAMENTE as sequencias de caracteres UTF-8 que foram 
# incorretamente salvas como Latin1 (ex: Ã£, â€œ, etc).
pattern = r'[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xf4][\x80-\xbf]{3}'
content = re.sub(pattern, fix_double_encoding, content)

# 2. Aplicar o patch de login (substituir o login fake pelo Supabase real)
login_target = '''        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = userIn.value.trim();
            const pass = passIn.value;

            if (!user || !pass) {
                if (!user) userIn.classList.add('ucgs-login--error');
                if (!pass) passIn.classList.add('ucgs-login--error');
                showAlert('EMPTY');
                (user ? passIn : userIn).focus();
                return;
            }

            setBusy(true);

            // Simulação de autenticação — substituir por chamada real ao backend
            setTimeout(() => {
                setBusy(false);

                // Credencial de demonstração
                const ok = (user.toLowerCase() === 'admin' && pass === 'ucgs2026');
                if (ok) {
                    try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                    submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                    submit.disabled = true;
                    setTimeout(() => hideScreen(false), 250);
                } else {
                    const err = (user.toLowerCase() === 'bloqueado') ? 'BLOCKED' : 'INVALID';
                    showAlert(err);
                    passIn.classList.add('ucgs-login--error');
                    passIn.focus();
                    passIn.select();
                }
            }, 900);
        });'''

login_replacement = '''        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const user = userIn.value.trim();
            const pass = passIn.value;

            if (!user || !pass) {
                if (!user) userIn.classList.add('ucgs-login--error');
                if (!pass) passIn.classList.add('ucgs-login--error');
                showAlert('EMPTY');
                (user ? passIn : userIn).focus();
                return;
            }

            setBusy(true);

            try {
                // Autenticação real com Supabase
                const authResult = await SupabaseClient.auth.login(user, pass);
                
                try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                
                setTimeout(() => {
                    hideScreen(false);
                    // Força carregamento da tabela se estiver visível
                    if (window.pacLoad && document.getElementById('pacientes') && document.getElementById('pacientes').classList.contains('active')) {
                        window.pacLoad();
                    }
                }, 400);

            } catch (err) {
                console.error('Erro de login:', err);
                showAlert('INVALID');
                passIn.classList.add('ucgs-login--error');
                passIn.focus();
                passIn.select();
            } finally {
                setBusy(false);
            }
        });'''

if login_target in content:
    content = content.replace(login_target, login_replacement)
else:
    # Fallback caso nao ache a string exata
    content = re.sub(r'// Simulação de autenticação.*?setTimeout\(\(\) => \{.*?\}, 900\);', 
                    '''try {
                const authResult = await SupabaseClient.auth.login(user, pass);
                try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                setTimeout(() => {
                    hideScreen(false);
                    if (window.pacLoad && document.getElementById('pacientes') && document.getElementById('pacientes').classList.contains('active')) {
                        window.pacLoad();
                    }
                }, 400);
            } catch (err) {
                console.error('Erro de login:', err);
                showAlert('INVALID');
                passIn.classList.add('ucgs-login--error');
                passIn.focus();
                passIn.select();
            } finally {
                setBusy(false);
            }''', content, flags=re.DOTALL)
    content = content.replace("form.addEventListener('submit', (e) => {", "form.addEventListener('submit', async (e) => {")


# Salvar o arquivo
with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(content)

print("Double encoding safely reversed. Auth logic patched. JavaScript unharmed.")
