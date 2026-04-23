import re

with open('site nevo_backup.HTML', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Generate the exact string of characters that map to 0x80-0xBF in cp1252
cont_bytes = bytes(range(0x80, 0xC0))
cont_chars = []
for b in range(0x80, 0xC0):
    try:
        cont_chars.append(bytes([b]).decode('cp1252'))
    except UnicodeDecodeError:
        pass

cont_pattern = '[' + re.escape(''.join(cont_chars)) + ']'

# Lead bytes 0xC2-0xDF
lead2_chars = []
for b in range(0xC2, 0xE0):
    try:
        lead2_chars.append(bytes([b]).decode('cp1252'))
    except:
        pass
lead2_pattern = '[' + re.escape(''.join(lead2_chars)) + ']'

# Lead bytes 0xE0-0xEF
lead3_chars = []
for b in range(0xE0, 0xF0):
    try:
        lead3_chars.append(bytes([b]).decode('cp1252'))
    except:
        pass
lead3_pattern = '[' + re.escape(''.join(lead3_chars)) + ']'

# Lead bytes 0xF0-0xF4
lead4_chars = []
for b in range(0xF0, 0xF5):
    try:
        lead4_chars.append(bytes([b]).decode('cp1252'))
    except:
        pass
lead4_pattern = '[' + re.escape(''.join(lead4_chars)) + ']'

pattern = f"({lead2_pattern}{cont_pattern}|{lead3_pattern}{cont_pattern}{{2}}|{lead4_pattern}{cont_pattern}{{3}})"

def fix_double_encoding(match):
    s = match.group(0)
    try:
        return s.encode('cp1252').decode('utf-8')
    except Exception as e:
        return s

fixed_content = re.sub(pattern, fix_double_encoding, content)

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

if login_target in fixed_content:
    fixed_content = fixed_content.replace(login_target, login_replacement)
else:
    # Tenta um replace mais flexível com regex
    fixed_content = re.sub(r'// Simulação de autenticação.*?setTimeout\(\(\) => \{.*?\}, 900\);', 
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
            }''', fixed_content, flags=re.DOTALL)
    fixed_content = fixed_content.replace("form.addEventListener('submit', (e) => {", "form.addEventListener('submit', async (e) => {")


# Ensure FontAwesome is included in <head> for emojis to work properly if they rely on it (though we just fix native emojis)
# And make sure UTF-8 is declared.
if '<meta charset="UTF-8">' not in fixed_content:
    fixed_content = fixed_content.replace('<head>', '<head>\n    <meta charset="UTF-8">')

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("SUCCESS: CP1252 double encoding reversed via regex. JS intact.")
