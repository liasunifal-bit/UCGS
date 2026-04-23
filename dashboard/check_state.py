with open(r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('pacientes-service', 'pacientes-service.js carregado no HTML'),
    ('window.PacientesService', 'window.PacientesService definido'),
    ('supabase-config', 'supabase-config.js carregado'),
    ('cdn.jsdelivr.net', 'SDK Supabase CDN carregado'),
    ('registerModal', 'Modal de cadastro presente'),
    ('_supa', 'Cliente _supa inicializado'),
]
for key, label in checks:
    status = 'SIM' if key in html else 'NAO'
    print(label + ': ' + status)
