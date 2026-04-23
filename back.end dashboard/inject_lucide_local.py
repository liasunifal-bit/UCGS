#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCGS – Fix icons usando Lucide LOCAL (sem CDN)
1. Usa backup como fonte limpa e corrige double-encoding via latin-1
2. Injeta lucide.min.js LOCAL (já baixado)
3. Substitui emojis quebrados por <i data-lucide="...">
4. Inicializa lucide.createIcons() ao final do body
"""
import re

SRC  = "site nevo_backup.HTML"
DEST = "site nevo.HTML"

with open(SRC, "r", encoding="utf-8-sig") as f:
    content = f.read()

# ── 1. Fix double-encoding via LATIN-1 (cobre TODOS os 256 bytes, sem exceções)
def fix_double(m):
    try:
        return m.group(0).encode("latin-1").decode("utf-8")
    except Exception:
        return m.group(0)

# Latin-1 mapeia direto: byte b -> chr(b), sem exceções
cont  = "".join(chr(b) for b in range(0x80, 0xC0))
lead2 = "".join(chr(b) for b in range(0xC2, 0xE0))
lead3 = "".join(chr(b) for b in range(0xE0, 0xF0))
lead4 = "".join(chr(b) for b in range(0xF0, 0xF5))

def cls(chars):
    return "[" + re.escape(chars) + "]"

pat = (f"(?:{cls(lead4)}{cls(cont)}{{3}}"
       f"|{cls(lead3)}{cls(cont)}{{2}}"
       f"|{cls(lead2)}{cls(cont)})")

content = re.sub(pat, fix_double, content)
print("[1] double-encoding (latin-1) corrigido")

# ── 2. meta charset
if '<meta charset="UTF-8">' not in content:
    content = content.replace("<head>", '<head>\n    <meta charset="UTF-8">', 1)
print("[2] meta charset OK")

# ── 3. Injetar Lucide LOCAL (+ FA como fallback)
LUCIDE_LOCAL = '\n    <script src="lucide.min.js"></script>\n'
FA_CDN = (
    '    <link rel="stylesheet" '
    'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" '
    'crossorigin="anonymous" referrerpolicy="no-referrer"/>\n'
)

if "lucide.min.js" not in content:
    content = content.replace("</head>", LUCIDE_LOCAL + FA_CDN + "</head>", 1)
    print("[3] Lucide LOCAL + FontAwesome injetados")

# ── 4. CSS para ícones
ICON_CSS = """
        /* ── Lucide SVG icons ── */
        i[data-lucide] { display:inline-flex; align-items:center; vertical-align:middle; }
        i[data-lucide] svg { width:1.1em; height:1.1em; stroke-width:2; }
        .sidebar i[data-lucide] svg,
        .nav-item i[data-lucide] svg { width:18px; height:18px; flex-shrink:0; }
        .stat-icon i[data-lucide] svg,
        .kpi-icon  i[data-lucide] svg { width:20px; height:20px; }
        .topbar-icon i[data-lucide] svg { width:20px; height:20px; }
        /* FA fallback */
        .nav-item .fa-solid, .nav-item .fa-regular { width:18px; text-align:center; }
"""
first_style_close = content.find("</style>")
if first_style_close > 0:
    content = content[:first_style_close] + ICON_CSS + content[first_style_close:]
print("[4] CSS de ícones injetado")

# ── 5. Substituição emoji → Lucide
ICON_MAP = [
    # Sidebar nav
    ("📊", '<i data-lucide="bar-chart-3"></i>'),
    ("👤", '<i data-lucide="user"></i>'),
    ("👥", '<i data-lucide="users"></i>'),
    ("📋", '<i data-lucide="clipboard-list"></i>'),
    ("🗺️",'<i data-lucide="map"></i>'),
    ("🗺", '<i data-lucide="map"></i>'),
    ("🔧", '<i data-lucide="wrench"></i>'),
    ("💉", '<i data-lucide="syringe"></i>'),
    ("🔬", '<i data-lucide="microscope"></i>'),
    ("⚠️",'<i data-lucide="triangle-alert"></i>'),
    ("⚠",  '<i data-lucide="triangle-alert"></i>'),
    ("🏥", '<i data-lucide="hospital"></i>'),
    ("🥗", '<i data-lucide="salad"></i>'),
    ("🩺", '<i data-lucide="stethoscope"></i>'),
    ("🦴", '<i data-lucide="bone"></i>'),
    ("🦷", '<i data-lucide="sparkles"></i>'),
    ("🧠", '<i data-lucide="brain"></i>'),
    ("📞", '<i data-lucide="phone"></i>'),
    ("📈", '<i data-lucide="trending-up"></i>'),
    ("📉", '<i data-lucide="trending-down"></i>'),
    ("📜", '<i data-lucide="scroll-text"></i>'),
    ("⚙️",'<i data-lucide="settings"></i>'),
    ("⚙",  '<i data-lucide="settings"></i>'),
    ("📅", '<i data-lucide="calendar"></i>'),
    ("🗓️",'<i data-lucide="calendar-days"></i>'),
    ("🗓", '<i data-lucide="calendar-days"></i>'),
    # Topbar / ações
    ("🔍", '<i data-lucide="search"></i>'),
    ("🔔", '<i data-lucide="bell"></i>'),
    ("🌓", '<i data-lucide="circle-half-stroke"></i>'),
    ("🌙", '<i data-lucide="moon"></i>'),
    ("☀️",'<i data-lucide="sun"></i>'),
    ("☀",  '<i data-lucide="sun"></i>'),
    ("🚪", '<i data-lucide="log-out"></i>'),
    ("✉",  '<i data-lucide="mail"></i>'),
    ("🪪", '<i data-lucide="id-card"></i>'),
    # Status
    ("✅", '<i data-lucide="circle-check"></i>'),
    ("⏳", '<i data-lucide="hourglass"></i>'),
    ("🚨", '<i data-lucide="siren"></i>'),
    # Módulos clínicos
    ("💊", '<i data-lucide="pill"></i>'),
    ("❤️",'<i data-lucide="heart"></i>'),
    ("❤",  '<i data-lucide="heart"></i>'),
    ("💪", '<i data-lucide="dumbbell"></i>'),
    ("❄️",'<i data-lucide="snowflake"></i>'),
    ("❄",  '<i data-lucide="snowflake"></i>'),
    ("📎", '<i data-lucide="paperclip"></i>'),
    ("🎯", '<i data-lucide="target"></i>'),
    ("⚡", '<i data-lucide="zap"></i>'),
    ("📐", '<i data-lucide="ruler"></i>'),
    ("🧮", '<i data-lucide="calculator"></i>'),
    ("🚫", '<i data-lucide="ban"></i>'),
    # Ações gerais
    ("✏️",'<i data-lucide="pen-line"></i>'),
    ("✏",  '<i data-lucide="pen-line"></i>'),
    ("📄", '<i data-lucide="file-text"></i>'),
    ("💾", '<i data-lucide="save"></i>'),
    ("🗑️",'<i data-lucide="trash-2"></i>'),
    ("🗑",  '<i data-lucide="trash-2"></i>'),
    ("➕", '<i data-lucide="plus"></i>'),
    ("➖", '<i data-lucide="minus"></i>'),
    ("🔄", '<i data-lucide="rotate-cw"></i>'),
    ("📤", '<i data-lucide="upload"></i>'),
    ("📥", '<i data-lucide="download"></i>'),
    ("🔐", '<i data-lucide="lock"></i>'),
    ("🔑", '<i data-lucide="key"></i>'),
    ("👁️",'<i data-lucide="eye"></i>'),
    ("👁",  '<i data-lucide="eye"></i>'),
    ("📍", '<i data-lucide="map-pin"></i>'),
    ("📝", '<i data-lucide="sticky-note"></i>'),
    ("🔗", '<i data-lucide="link"></i>'),
    ("ℹ️",'<i data-lucide="info"></i>'),
    ("ℹ",  '<i data-lucide="info"></i>'),
    ("🏷️",'<i data-lucide="tag"></i>'),
    ("🏷",  '<i data-lucide="tag"></i>'),
    ("🔪", '<i data-lucide="flame"></i>'),
    ("🧪", '<i data-lucide="flask-conical"></i>'),
    ("📗", '<i data-lucide="book-open"></i>'),
    ("🏃", '<i data-lucide="person-standing"></i>'),
    ("🧘", '<i data-lucide="person-standing"></i>'),
    # Toast symbols - manter como texto
    ("✓",  "✓"),
    ("✕",  "✕"),
    ("✔️", "✔"),
    ("✔",  "✔"),
    ("✖",  "✗"),
]

replaced_count = 0
for emoji, tag in ICON_MAP:
    n = content.count(emoji)
    if n > 0:
        content = content.replace(emoji, tag)
        replaced_count += n

print(f"[5] {replaced_count} emojis substituídos por Lucide icons")

# ── 6. Inicializar Lucide após DOM + após cada navegação dinâmica
LUCIDE_INIT = """
    <script>
    (function() {
        function initLucide() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
        // Inicializa ao carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initLucide);
        } else {
            initLucide();
        }
        // Re-inicializa ao mudar de aba (caso o sistema use SPA)
        window._lucideRefresh = initLucide;
        document.addEventListener('click', function(e) {
            var navItem = e.target.closest('[data-section], .nav-item, [onclick]');
            if (navItem) {
                setTimeout(initLucide, 100);
            }
        });
    })();
    </script>
"""

if "lucide.createIcons" not in content:
    content = content.replace("</body>", LUCIDE_INIT + "</body>", 1)
    print("[6] lucide.createIcons() inicializado")

# ── 7. Patch do login (fake → Supabase)
if "form.addEventListener('submit', (e) =>" in content and "Simulação de autenticação" in content:
    content = content.replace(
        "form.addEventListener('submit', (e) => {",
        "form.addEventListener('submit', async (e) => {", 1
    )
    old_block = re.search(
        r"// Simulação de autenticação.*?}, 900\);",
        content, re.DOTALL
    )
    if old_block:
        new_block = """try {
                const authResult = await SupabaseClient.auth.login(user, pass);
                try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                setBusy(false);
                setTimeout(() => {
                    hideScreen(false);
                    if (window._lucideRefresh) window._lucideRefresh();
                    if (window.pacLoad && document.getElementById('pacientes') &&
                        document.getElementById('pacientes').classList.contains('active')) {
                        window.pacLoad();
                    }
                }, 400);
            } catch (err) {
                console.error('Erro de login:', err);
                showAlert('INVALID');
                passIn.classList.add('ucgs-login--error');
                passIn.focus();
                passIn.select();
                setBusy(false);
            }"""
        content = content[:old_block.start()] + new_block + content[old_block.end():]
        print("[7] Login fake -> Supabase OK")

# ── 8. Salvar
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n[OK] {DEST} salvo ({len(content):,} chars)")
print("Abra http://localhost:8000/site%20nevo.HTML e pressione Ctrl+F5")
