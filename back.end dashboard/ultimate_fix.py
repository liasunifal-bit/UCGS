import re

# 1. Ler o backup com utf-8-sig para remover o BOM automaticamente
with open('site nevo_backup.HTML', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 2. Injetar <meta charset="UTF-8"> e FontAwesome se nao existirem
if '<meta charset="UTF-8">' not in content:
    content = re.sub(r'(<head.*?>)', r'\1\n    <meta charset="UTF-8">', content, count=1, flags=re.IGNORECASE)

fa_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">'
if fa_link not in content:
    content = re.sub(r'(<head.*?>)', r'\1\n    ' + fa_link, content, count=1, flags=re.IGNORECASE)

# 3. Aplicar o patch de login (substituir o login fake pelo Supabase real)
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
    # Fallback regex search if exact string matching fails due to line endings
    content = re.sub(r'// Simulação de autenticação.*?setTimeout\(\(\) => \{.*?\}, 900\);', 
                    '''try {
                // Autenticação real com Supabase
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

# 4. Substituir TODOS os emojis e icones de alta unicode por entidades HTML (seguro contra qquer charset)
out = []
for c in content:
    # Todos caracteres > 255 sao convertidos em &#xHEX;
    # 0x0100 to 0x10FFFF includes all non-latin characters, emojis, symbols, etc.
    # Excludes 0x00-0xFF which is ASCII + Latin-1 (so 'ã', 'ç', 'é' stay as literal utf-8 characters)
    if ord(c) > 0x00FF:
        out.append(f'&#x{ord(c):X};')
    else:
        out.append(c)

final_content = ''.join(out)

# 5. Salvar como site nevo.HTML forcando UTF-8 puro (sem BOM)
with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Restored from backup, patched auth, removed BOM, added FontAwesome, encoded emojis to HTML entities.")
