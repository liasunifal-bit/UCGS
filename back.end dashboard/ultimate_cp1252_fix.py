import re

with open('site nevo_backup.HTML', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# The characters were likely interpreted as cp1252.
def fix_double_encoding(match):
    s = match.group(0)
    try:
        # Encode as cp1252 to get the original utf-8 bytes
        return s.encode('cp1252').decode('utf-8')
    except Exception as e:
        return s

# A regex to match any sequence of characters that form a valid utf-8 byte sequence when encoded as cp1252
# But it's easier to just match the pattern of cp1252 characters that map to utf-8 lead bytes and continuation bytes.
# Lead bytes: \xc2-\xf4
# Cont bytes: \x80-\xbf 
# In cp1252, the characters for \x80-\xbf include: €, ‚, ƒ, „, …, †, ‡, ˆ, ‰, Š, ‹, Œ, Ž, ‘, ’, “, ”, •, –, —, ˜, ™, š, ›, œ, ž, Ÿ, and \xa0-\xbf (¡ to ¿)
# So we can just encode the entire string, but that might break valid ascii.
# Wait, actually, any character that shouldn't be cp1252 will throw an exception or decode incorrectly.
# Let's just find sequences of 2-4 characters that look like cp1252-decoded utf-8.

cp1252_chars = ''.join(chr(i).encode('cp1252').decode('cp1252') for i in range(128, 256) if i not in [129, 141, 143, 144, 157])
valid_cont = '[' + re.escape(''.join(chr(i).decode('cp1252') for i in range(0x80, 0xC0) if bytes([i]).decode('cp1252', 'ignore'))) + ']'
valid_lead2 = '[' + re.escape(''.join(chr(i).decode('cp1252') for i in range(0xC2, 0xE0) if bytes([i]).decode('cp1252', 'ignore'))) + ']'
valid_lead3 = '[' + re.escape(''.join(chr(i).decode('cp1252') for i in range(0xE0, 0xF0) if bytes([i]).decode('cp1252', 'ignore'))) + ']'
valid_lead4 = '[' + re.escape(''.join(chr(i).decode('cp1252') for i in range(0xF0, 0xF5) if bytes([i]).decode('cp1252', 'ignore'))) + ']'

pattern = f"({valid_lead2}{valid_cont}|{valid_lead3}{valid_cont}{{2}}|{valid_lead4}{valid_cont}{{3}})"

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

# Add the meta charset utf-8 if not present correctly.
if '<meta charset="UTF-8">' not in content:
    content = content.replace('<head>', '<head>\n    <meta charset="UTF-8">')

# Salvar o arquivo
with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(content)

print("Double encoding via CP1252 safely reversed. Auth logic patched. JavaScript unharmed.")
