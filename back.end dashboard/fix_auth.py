import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'    // ============================================================\n    // LOGOUT.*?console\.error\("Erro no login Supabase:", err\);\n                \}\);\n        \};', re.DOTALL)

replacement = """    const authenticate = () => {
        setBusy(true);
        const user = userIn.value.trim();
        const pass = passIn.value;
        if(!user || !pass) {
            setBusy(false);
            return;
        }
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
            });
    };

    submit.addEventListener('click', (e) => {
        e.preventDefault();
        authenticate();
    });

    // ============================================================
    // LOGOUT
    // ============================================================
    document.getElementById('logoutBtn').addEventListener('click', () => {
        closeUserDropdown();
        const confirmed = confirm('Deseja realmente sair do sistema?');
        if (!confirmed) return;
        const logoutBtn = document.getElementById('logoutBtn');
        logoutBtn.classList.add('logout-loading');
        setTimeout(() => {
            logoutBtn.classList.remove('logout-loading');
            try { sessionStorage.removeItem(SESSION_KEY); } catch (e) {}
            window.location.reload();
        }, 900);
    });"""

new_content = pattern.sub(replacement, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Injecao corrigida com sucesso.")
