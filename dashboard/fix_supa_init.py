import re

def fix_supa_init():
    path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Find the Supabase SDK + Auth Handlers block and remove it
    html = re.sub(
        r'\s*<!-- Supabase SDK \+ Auth Handlers -->.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    # 2. Build a new, reliable block that waits for the SDK to load
    SUPABASE_URL = 'https://llqphjlpypnyvknpfdyn.supabase.co'
    SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxscXBoamxweXBueXZrbnBmZHluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MzM0MjksImV4cCI6MjA5MjEwOTQyOX0.h_ycCGtWgnzB5CtM-dXv1BlUt-iIN0RxyuGnAJBkbow'

    new_block = f"""
    <!-- Supabase SDK + Auth Handlers -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" onload="initSupabase()" onerror="console.error('Supabase CDN failed to load')"></script>
    <script>
    function initSupabase() {{
        try {{
            window._supa = supabase.createClient(
                '{SUPABASE_URL}',
                '{SUPABASE_ANON_KEY}'
            );
            console.log('[UCGS] Supabase client initialized:', !!window._supa);

            // Auth state listener - hides login overlay when user is authenticated
            window._supa.auth.onAuthStateChange(function(event, session) {{
                console.log('[UCGS] Auth event:', event, !!session);
                var overlay = document.getElementById('authOverlay');
                if (session && overlay) {{
                    overlay.style.transition = 'opacity 0.5s';
                    overlay.style.opacity = '0';
                    setTimeout(function() {{ overlay.style.display = 'none'; }}, 500);
                }}
            }});

            // Expose PacientesService globally using the initialized client
            if (typeof PacientesServiceFactory === 'function') {{
                window.PacientesService = PacientesServiceFactory(window._supa);
            }}

        }} catch(e) {{
            console.error('[UCGS] Failed to initialize Supabase:', e);
        }}
    }}

    // Fallback: if onload already fired (cached script), init immediately
    document.addEventListener('DOMContentLoaded', function() {{
        if (typeof supabase !== 'undefined' && !window._supa) {{
            initSupabase();
        }}
    }});

    document.addEventListener('DOMContentLoaded', function() {{
        var submitBtn   = document.getElementById('submitBtn');
        var userInput   = document.getElementById('userInput');
        var passInput   = document.getElementById('passwordInput');
        var alertBox    = document.getElementById('formAlert');
        var alertTitle  = document.getElementById('formAlertTitle');
        var alertMsg    = document.getElementById('formAlertMsg');
        var toggleBtn   = document.getElementById('togglePassword');
        var eyeIcon     = document.getElementById('eyeIcon');

        function showAlert(title, msg, isSuccess) {{
            if (!alertBox) return;
            if (alertTitle) alertTitle.textContent = title;
            if (alertMsg)   alertMsg.textContent   = msg;
            alertBox.classList.add('visible');
            alertBox.style.borderLeftColor = isSuccess ? '#10B981' : '#EF4444';
        }}

        function setLoading(loading) {{
            [submitBtn, userInput, passInput].forEach(function(el) {{
                if (el) el.disabled = loading;
            }});
        }}

        // Toggle password visibility
        if (toggleBtn && passInput) {{
            toggleBtn.addEventListener('click', function() {{
                var visible = passInput.type === 'text';
                passInput.type = visible ? 'password' : 'text';
                if (eyeIcon) {{
                    eyeIcon.innerHTML = visible
                        ? '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>'
                        : '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
                }}
            }});
        }}

        // LOGIN
        if (submitBtn) {{
            submitBtn.addEventListener('click', async function(e) {{
                e.preventDefault();
                if (!window._supa) {{ showAlert('Erro de conexao.', 'Aguarde e tente novamente.', false); return; }}
                var email = userInput ? userInput.value.trim() : '';
                var pass  = passInput ? passInput.value : '';
                if (!email || !pass) {{
                    showAlert('Campos obrigatorios.', 'Informe e-mail e senha para continuar.', false);
                    return;
                }}
                setLoading(true);
                try {{
                    var r = await window._supa.auth.signInWithPassword({{ email: email, password: pass }});
                    if (r.error) throw r.error;
                    showAlert('Login realizado!', 'Autenticado. Carregando painel...', true);
                }} catch(err) {{
                    showAlert('Credenciais incorretas.', err.message || 'Verifique e-mail e senha.', false);
                }} finally {{
                    setLoading(false);
                }}
            }});
        }}
    }});
    </script>
"""

    # 3. Insert before </body>
    html = html.replace('</body>', new_block + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Supabase initialization fixed with onload guarantee!")

if __name__ == '__main__':
    fix_supa_init()
