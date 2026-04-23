import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''// Autenticação Real no Supabase
            SupabaseClient.auth.login(user, pass)
                .then(data => {
                    setBusy(false);
                    try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                    submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                    submit.disabled = true;
                    
                    const dUser = document.querySelector('.user-info h3');
                    if(dUser) dUser.textContent = user;
                    const dRole = document.querySelector('.user-info p');
                    if(dRole) dRole.textContent = 'Autenticado';
                        
                    setTimeout(() => hideScreen(false), 250);
                })
                .catch(err => {
                    setBusy(false);
                    showAlert('INVALID');
                    alertM.textContent = 'E-mail ou senha incorretos.';
                    passIn.classList.add('ucgs-login--error');
                    passIn.focus();
                    passIn.select();
                    console.error("Erro no login Supabase:", err);
                });'''

idx = content.find('// Simula')
if idx != -1:
    end_idx = content.find('}, 900);', idx)
    if end_idx != -1:
        new_content = content[:idx] + replacement + content[end_idx+8:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Injeção de login do Supabase concluída.")
    else:
        print("ERRO: Fim do bloco não encontrado.")
else:
    print("ERRO: Início do bloco não encontrado.")

