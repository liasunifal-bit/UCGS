#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCGS Icon Fix — Abordagem SVG inline via Lucide
1. Usa backup como fonte limpa
2. Corrige double-encoding cp1252->utf-8
3. Injeta Lucide Icons (CDN JS, renderiza SVG via JS)
4. Substitui emojis por <i data-lucide="..."> tags
5. Garante que o script Lucide inicializa após o DOM
"""
import re

SRC  = "site nevo_backup.HTML"
DEST = "site nevo.HTML"

with open(SRC, "r", encoding="utf-8-sig") as f:
    content = f.read()

# ── 1. Fix double-encoding (cp1252 → utf-8) ─────────────────────
def cp1252_range(lo, hi):
    chars = []
    for b in range(lo, hi):
        try:
            chars.append(bytes([b]).decode("cp1252"))
        except Exception:
            pass
    return chars

cont  = cp1252_range(0x80, 0xC0)
lead2 = cp1252_range(0xC2, 0xE0)
lead3 = cp1252_range(0xE0, 0xF0)
lead4 = cp1252_range(0xF0, 0xF5)

def cls(chars):
    return "[" + re.escape("".join(chars)) + "]"

pat = (f"(?:{cls(lead4)}{cls(cont)}{{3}}"
       f"|{cls(lead3)}{cls(cont)}{{2}}"
       f"|{cls(lead2)}{cls(cont)})")

def fix_double(m):
    try:
        return m.group(0).encode("cp1252").decode("utf-8")
    except Exception:
        return m.group(0)

content = re.sub(pat, fix_double, content)
print("[1] double-encoding corrigido")

# ── 2. Garantir meta charset ─────────────────────────────────────
if '<meta charset="UTF-8">' not in content:
    content = content.replace("<head>", '<head>\n    <meta charset="UTF-8">', 1)
print("[2] meta charset OK")

# ── 3. Injetar Lucide Icons CDN (SVG via JS) ─────────────────────
LUCIDE_CDN = (
    '\n    <!-- Lucide Icons (SVG, sem dependência de fonte) -->\n'
    '    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n'
)

# Injetar também FontAwesome como fallback alternativo
FA_CDN = (
    '\n    <!-- FontAwesome 6 Free -->\n'
    '    <link rel="stylesheet" '
    'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" '
    'crossorigin="anonymous" referrerpolicy="no-referrer"/>\n'
)

if "lucide" not in content.lower():
    content = content.replace("</head>", LUCIDE_CDN + FA_CDN + "</head>", 1)
    print("[3] Lucide + FontAwesome injetados")
else:
    print("[3] Lucide ja presente")

# ── 4. CSS para ícones ───────────────────────────────────────────
ICON_CSS = """
        /* ── Lucide SVG icon sizing ── */
        i[data-lucide] svg, .lucide {
            width: 1em;
            height: 1em;
            stroke-width: 2;
            vertical-align: middle;
            display: inline-block;
        }
        .nav-icon-wrap i[data-lucide] svg,
        .sidebar i[data-lucide] svg {
            width: 18px;
            height: 18px;
        }
        .stat-icon i[data-lucide] svg { width: 20px; height: 20px; }
        /* FA fallback */
        .nav-item .fas, .nav-item .fa-solid,
        .nav-item .far, .nav-item .fa-regular {
            width: 18px; text-align: center; font-size: 1rem;
        }
"""
first_style_close = content.find("</style>")
if first_style_close > 0:
    content = content[:first_style_close] + ICON_CSS + content[first_style_close:]
print("[4] CSS de ícones injetado")

# ── 5. Mapeamento emoji → Lucide tag ─────────────────────────────
# Usamos <i data-lucide="nome"> que o Lucide.js converte para SVG no DOMContentLoaded
ICON_MAP = [
    # Sidebar
    ("📊", '<i data-lucide="bar-chart-3" aria-hidden="true"></i>'),
    ("👤", '<i data-lucide="user" aria-hidden="true"></i>'),
    ("👥", '<i data-lucide="users" aria-hidden="true"></i>'),
    ("📋", '<i data-lucide="clipboard-list" aria-hidden="true"></i>'),
    ("🗺️",'<i data-lucide="map" aria-hidden="true"></i>'),
    ("🗺", '<i data-lucide="map" aria-hidden="true"></i>'),
    ("🔧", '<i data-lucide="wrench" aria-hidden="true"></i>'),
    ("💉", '<i data-lucide="syringe" aria-hidden="true"></i>'),
    ("🔬", '<i data-lucide="microscope" aria-hidden="true"></i>'),
    ("⚠️",'<i data-lucide="triangle-alert" aria-hidden="true"></i>'),
    ("⚠",  '<i data-lucide="triangle-alert" aria-hidden="true"></i>'),
    ("🏥", '<i data-lucide="hospital" aria-hidden="true"></i>'),
    ("🥗", '<i data-lucide="salad" aria-hidden="true"></i>'),
    ("🩺", '<i data-lucide="stethoscope" aria-hidden="true"></i>'),
    ("🦴", '<i data-lucide="bone" aria-hidden="true"></i>'),
    ("🦷", '<i data-lucide="smile" aria-hidden="true"></i>'),  # sem ícone de dente no Lucide
    ("🧠", '<i data-lucide="brain" aria-hidden="true"></i>'),
    ("📞", '<i data-lucide="phone" aria-hidden="true"></i>'),
    ("📈", '<i data-lucide="trending-up" aria-hidden="true"></i>'),
    ("📉", '<i data-lucide="trending-down" aria-hidden="true"></i>'),
    ("⚙️",'<i data-lucide="settings" aria-hidden="true"></i>'),
    ("⚙",  '<i data-lucide="settings" aria-hidden="true"></i>'),
    ("📅", '<i data-lucide="calendar" aria-hidden="true"></i>'),
    ("🗓️",'<i data-lucide="calendar-days" aria-hidden="true"></i>'),
    ("🗓",  '<i data-lucide="calendar-days" aria-hidden="true"></i>'),
    # Topbar
    ("🔍", '<i data-lucide="search" aria-hidden="true"></i>'),
    ("🔔", '<i data-lucide="bell" aria-hidden="true"></i>'),
    ("🌓", '<i data-lucide="circle-half" aria-hidden="true"></i>'),
    ("🌙", '<i data-lucide="moon" aria-hidden="true"></i>'),
    ("☀️",'<i data-lucide="sun" aria-hidden="true"></i>'),
    ("☀",  '<i data-lucide="sun" aria-hidden="true"></i>'),
    ("🚪", '<i data-lucide="log-out" aria-hidden="true"></i>'),
    ("✉",  '<i data-lucide="mail" aria-hidden="true"></i>'),
    ("🪪", '<i data-lucide="id-card" aria-hidden="true"></i>'),
    # Status
    ("✅", '<i data-lucide="circle-check" aria-hidden="true"></i>'),
    ("⏳", '<i data-lucide="hourglass" aria-hidden="true"></i>'),
    ("🚨", '<i data-lucide="siren" aria-hidden="true"></i>'),
    # Clínicos
    ("💊", '<i data-lucide="pill" aria-hidden="true"></i>'),
    ("❤️",'<i data-lucide="heart" aria-hidden="true"></i>'),
    ("❤",  '<i data-lucide="heart" aria-hidden="true"></i>'),
    ("💪", '<i data-lucide="dumbbell" aria-hidden="true"></i>'),
    ("❄️",'<i data-lucide="snowflake" aria-hidden="true"></i>'),
    ("❄",  '<i data-lucide="snowflake" aria-hidden="true"></i>'),
    ("📎", '<i data-lucide="paperclip" aria-hidden="true"></i>'),
    ("🎯", '<i data-lucide="target" aria-hidden="true"></i>'),
    ("⚡", '<i data-lucide="zap" aria-hidden="true"></i>'),
    ("📐", '<i data-lucide="ruler" aria-hidden="true"></i>'),
    ("🧮", '<i data-lucide="calculator" aria-hidden="true"></i>'),
    ("🚫", '<i data-lucide="ban" aria-hidden="true"></i>'),
    # Ações
    ("✏️",'<i data-lucide="pen-line" aria-hidden="true"></i>'),
    ("✏",  '<i data-lucide="pen-line" aria-hidden="true"></i>'),
    ("📄", '<i data-lucide="file-text" aria-hidden="true"></i>'),
    ("💾", '<i data-lucide="save" aria-hidden="true"></i>'),
    ("🗑️",'<i data-lucide="trash-2" aria-hidden="true"></i>'),
    ("🗑",  '<i data-lucide="trash-2" aria-hidden="true"></i>'),
    ("➕", '<i data-lucide="plus" aria-hidden="true"></i>'),
    ("➖", '<i data-lucide="minus" aria-hidden="true"></i>'),
    ("🔄", '<i data-lucide="rotate-cw" aria-hidden="true"></i>'),
    ("📤", '<i data-lucide="upload" aria-hidden="true"></i>'),
    ("📥", '<i data-lucide="download" aria-hidden="true"></i>'),
    ("🔐", '<i data-lucide="lock" aria-hidden="true"></i>'),
    ("🔑", '<i data-lucide="key" aria-hidden="true"></i>'),
    ("👁️",'<i data-lucide="eye" aria-hidden="true"></i>'),
    ("👁",  '<i data-lucide="eye" aria-hidden="true"></i>'),
    ("📍", '<i data-lucide="map-pin" aria-hidden="true"></i>'),
    ("📝", '<i data-lucide="sticky-note" aria-hidden="true"></i>'),
    ("🔗", '<i data-lucide="link" aria-hidden="true"></i>'),
    ("ℹ️",'<i data-lucide="info" aria-hidden="true"></i>'),
    ("ℹ",  '<i data-lucide="info" aria-hidden="true"></i>'),
    ("🏷️",'<i data-lucide="tag" aria-hidden="true"></i>'),
    ("🏷",  '<i data-lucide="tag" aria-hidden="true"></i>'),
    ("🔪", '<i data-lucide="flame" aria-hidden="true"></i>'),
    # Toast symbols — keep visíveis como texto
    ("✓",  "✓"),
    ("✕",  "✕"),
    ("✔️", "✔"),
    ("✔",  "✔"),
]

replaced_count = 0
for emoji, tag in ICON_MAP:
    n = content.count(emoji)
    if n > 0:
        content = content.replace(emoji, tag)
        replaced_count += n
        print(f"  {emoji} → lucide ({n}x)")

print(f"[5] {replaced_count} emojis substituídos por Lucide icons")

# ── 6. Inicializar Lucide após DOM pronto ─────────────────────────
LUCIDE_INIT = """
    <script>
        // Inicializa Lucide Icons após carregamento completo do DOM
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
                // Re-inicializar quando conteúdo dinâmico for adicionado
                const _origCreateIcons = lucide.createIcons.bind(lucide);
                window._lucideRefresh = function() { _origCreateIcons(); };
            }
        });
    </script>
"""

# Inserir antes de </body>
if "lucide.createIcons" not in content:
    content = content.replace("</body>", LUCIDE_INIT + "</body>", 1)
    print("[6] lucide.createIcons() injetado")

# ── 7. Patch do login ─────────────────────────────────────────────
if "form.addEventListener('submit', (e) => {" in content and "Simulação de autenticação" in content:
    content = content.replace(
        "form.addEventListener('submit', (e) => {",
        "form.addEventListener('submit', async (e) => {",
        1
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
                setTimeout(() => {
                    hideScreen(false);
                    if (window.pacLoad && document.getElementById('pacientes') &&
                        document.getElementById('pacientes').classList.contains('active')) {
                        window.pacLoad();
                    }
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                }, 400);
            } catch (err) {
                console.error('Erro de login:', err);
                showAlert('INVALID');
                passIn.classList.add('ucgs-login--error');
                passIn.focus();
                passIn.select();
            } finally {
                setBusy(false);
            }"""
        content = content[:old_block.start()] + new_block + content[old_block.end():]
        print("[7] Login fake substituído por Supabase auth")

# ── 8. Salvar ─────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n[OK] Salvo em {DEST} ({len(content):,} chars)")
