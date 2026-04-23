#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCGS Dashboard – Icon Integration + Encoding Fix
Usa o backup limpo como fonte, injeta FontAwesome 6 e substitui
emojis do sidebar/topbar por <i> tags FA consistentes.
"""
import re, sys

# ── 1. Carregar arquivo ──────────────────────────────────────────
SRC  = "site nevo_backup.HTML"
DEST = "site nevo.HTML"

with open(SRC, "r", encoding="utf-8-sig") as f:
    content = f.read()

# ── 2. Reverter double-encoding cp1252 → utf-8 ──────────────────
def fix_double(m):
    try:
        return m.group(0).encode("cp1252").decode("utf-8")
    except Exception:
        return m.group(0)

# Gera os chars cp1252 que correspondem aos lead/cont bytes utf-8
def cp1252_chars_for_range(lo, hi):
    chars = []
    for b in range(lo, hi):
        try:
            chars.append(bytes([b]).decode("cp1252"))
        except Exception:
            pass
    return chars

cont  = cp1252_chars_for_range(0x80, 0xC0)
lead2 = cp1252_chars_for_range(0xC2, 0xE0)
lead3 = cp1252_chars_for_range(0xE0, 0xF0)
lead4 = cp1252_chars_for_range(0xF0, 0xF5)

def cls(chars):
    return "[" + re.escape("".join(chars)) + "]"

pat = (f"(?:{cls(lead4)}{cls(cont)}{{3}}"
       f"|{cls(lead3)}{cls(cont)}{{2}}"
       f"|{cls(lead2)}{cls(cont)})")

content = re.sub(pat, fix_double, content)
print("✓ double-encoding corrigido")

# ── 3. Garantir meta charset UTF-8 ──────────────────────────────
if '<meta charset="UTF-8">' not in content:
    content = content.replace("<head>", '<head>\n    <meta charset="UTF-8">', 1)
print("✓ meta charset OK")

# ── 4. Injetar FontAwesome 6 Free + Lucide (SVG sprite) ─────────
FA_LINK = (
    '\n    <!-- FontAwesome 6 Free -->\n'
    '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/'
    'font-awesome/6.5.2/css/all.min.css" '
    'integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W==" '
    'crossorigin="anonymous" referrerpolicy="no-referrer"/>\n'
)

if "font-awesome" not in content.lower():
    # Inserir antes do </head>
    content = content.replace("</head>", FA_LINK + "</head>", 1)
    print("✓ FontAwesome 6 injetado")
else:
    print("✓ FontAwesome já presente")

# ── 5. CSS extra para ícones FA no sidebar ───────────────────────
FA_CSS = """
        /* ── FontAwesome icon sizing inside sidebar nav ── */
        .sidebar .nav-icon, .sidebar .nav-item > i,
        .nav-item .fa, .nav-item .fas, .nav-item .far,
        .nav-item .fab, .nav-item .fa-solid, .nav-item .fa-regular {
            width: 20px;
            font-size: 1rem;
            text-align: center;
            flex-shrink: 0;
            opacity: 0.85;
            transition: opacity 0.2s;
        }
        .nav-item.active .fa, .nav-item.active .fas,
        .nav-item.active .fa-solid { opacity: 1; }
        .topbar-action-btn i { font-size: 1rem; }
        /* Dashboard stat card icons */
        .stat-icon i, .kpi-icon i { font-size: 1.25rem; }
"""

# Inserir o bloco CSS antes de </style> (primeira ocorrência)
first_style_close = content.find("</style>")
if first_style_close > 0:
    content = content[:first_style_close] + FA_CSS + content[first_style_close:]
print("✓ CSS de ícones injetado")

# ── 6. Mapeamento Emoji → FA icon (sidebar + topbar) ─────────────
# Formato: (padrão_a_substituir, substituição)
# Apenas dentro de spans/ícones do sidebar - usamos replace simples nos emojis

ICON_MAP = [
    # Sidebar
    ("📊", '<i class="fa-solid fa-chart-bar" aria-hidden="true"></i>'),
    ("👤", '<i class="fa-solid fa-user" aria-hidden="true"></i>'),
    ("📋", '<i class="fa-solid fa-clipboard-list" aria-hidden="true"></i>'),
    ("🗺️", '<i class="fa-solid fa-map" aria-hidden="true"></i>'),
    ("🗺",  '<i class="fa-solid fa-map" aria-hidden="true"></i>'),
    ("🔧", '<i class="fa-solid fa-wrench" aria-hidden="true"></i>'),
    ("💉", '<i class="fa-solid fa-syringe" aria-hidden="true"></i>'),
    ("🔬", '<i class="fa-solid fa-microscope" aria-hidden="true"></i>'),
    ("⚠️", '<i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>'),
    ("⚠",  '<i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>'),
    ("🏥", '<i class="fa-solid fa-hospital" aria-hidden="true"></i>'),
    ("🥗", '<i class="fa-solid fa-bowl-food" aria-hidden="true"></i>'),
    ("🩺", '<i class="fa-solid fa-stethoscope" aria-hidden="true"></i>'),
    ("🦴", '<i class="fa-solid fa-bone" aria-hidden="true"></i>'),
    ("🦷", '<i class="fa-solid fa-tooth" aria-hidden="true"></i>'),
    ("🧠", '<i class="fa-solid fa-brain" aria-hidden="true"></i>'),
    ("📞", '<i class="fa-solid fa-phone" aria-hidden="true"></i>'),
    ("📈", '<i class="fa-solid fa-chart-line" aria-hidden="true"></i>'),
    ("⚙️", '<i class="fa-solid fa-gear" aria-hidden="true"></i>'),
    ("⚙",  '<i class="fa-solid fa-gear" aria-hidden="true"></i>'),
    # Topbar / ações
    ("🔍", '<i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>'),
    ("🔔", '<i class="fa-solid fa-bell" aria-hidden="true"></i>'),
    ("🌓", '<i class="fa-solid fa-circle-half-stroke" aria-hidden="true"></i>'),
    ("🌙", '<i class="fa-solid fa-moon" aria-hidden="true"></i>'),
    ("☀️", '<i class="fa-solid fa-sun" aria-hidden="true"></i>'),
    ("☀",  '<i class="fa-solid fa-sun" aria-hidden="true"></i>'),
    ("🚪", '<i class="fa-solid fa-right-from-bracket" aria-hidden="true"></i>'),
    ("✉",  '<i class="fa-solid fa-envelope" aria-hidden="true"></i>'),
    ("🪪", '<i class="fa-solid fa-id-card" aria-hidden="true"></i>'),
    # Dashboard
    ("✅", '<i class="fa-solid fa-circle-check" style="color:var(--success)" aria-hidden="true"></i>'),
    ("⏳", '<i class="fa-solid fa-hourglass-half" style="color:var(--warning)" aria-hidden="true"></i>'),
    ("🚨", '<i class="fa-solid fa-siren-on" style="color:var(--danger)" aria-hidden="true"></i>'),
    ("📅", '<i class="fa-regular fa-calendar" aria-hidden="true"></i>'),
    # Módulos clínicos
    ("💊", '<i class="fa-solid fa-pills" aria-hidden="true"></i>'),
    ("❤️", '<i class="fa-solid fa-heart" style="color:#ef4444" aria-hidden="true"></i>'),
    ("❤",  '<i class="fa-solid fa-heart" style="color:#ef4444" aria-hidden="true"></i>'),
    ("💪", '<i class="fa-solid fa-dumbbell" aria-hidden="true"></i>'),
    ("❄️", '<i class="fa-solid fa-snowflake" aria-hidden="true"></i>'),
    ("❄",  '<i class="fa-solid fa-snowflake" aria-hidden="true"></i>'),
    ("📎", '<i class="fa-solid fa-paperclip" aria-hidden="true"></i>'),
    ("🎯", '<i class="fa-solid fa-bullseye" aria-hidden="true"></i>'),
    ("⚡", '<i class="fa-solid fa-bolt" aria-hidden="true"></i>'),
    ("📐", '<i class="fa-solid fa-ruler" aria-hidden="true"></i>'),
    ("🧮", '<i class="fa-solid fa-calculator" aria-hidden="true"></i>'),
    ("🚫", '<i class="fa-solid fa-ban" aria-hidden="true"></i>'),
    # Ações inline
    ("✏️", '<i class="fa-solid fa-pen-to-square" aria-hidden="true"></i>'),
    ("✏",  '<i class="fa-solid fa-pen-to-square" aria-hidden="true"></i>'),
    ("📄", '<i class="fa-regular fa-file-lines" aria-hidden="true"></i>'),
    ("💾", '<i class="fa-solid fa-floppy-disk" aria-hidden="true"></i>'),
    ("🗑️", '<i class="fa-solid fa-trash" aria-hidden="true"></i>'),
    ("🗑",  '<i class="fa-solid fa-trash" aria-hidden="true"></i>'),
    ("➕", '<i class="fa-solid fa-plus" aria-hidden="true"></i>'),
    ("➖", '<i class="fa-solid fa-minus" aria-hidden="true"></i>'),
    ("🔄", '<i class="fa-solid fa-rotate" aria-hidden="true"></i>'),
    ("📤", '<i class="fa-solid fa-upload" aria-hidden="true"></i>'),
    ("📥", '<i class="fa-solid fa-download" aria-hidden="true"></i>'),
    ("🏷️", '<i class="fa-solid fa-tag" aria-hidden="true"></i>'),
    ("🏷",  '<i class="fa-solid fa-tag" aria-hidden="true"></i>'),
    ("🔐", '<i class="fa-solid fa-lock" aria-hidden="true"></i>'),
    ("🔑", '<i class="fa-solid fa-key" aria-hidden="true"></i>'),
    ("👁️", '<i class="fa-solid fa-eye" aria-hidden="true"></i>'),
    ("👁",  '<i class="fa-solid fa-eye" aria-hidden="true"></i>'),
    ("👥", '<i class="fa-solid fa-users" aria-hidden="true"></i>'),
    ("📍", '<i class="fa-solid fa-location-dot" aria-hidden="true"></i>'),
    ("🕐", '<i class="fa-regular fa-clock" aria-hidden="true"></i>'),
    ("🕑", '<i class="fa-regular fa-clock" aria-hidden="true"></i>'),
    ("⏰", '<i class="fa-regular fa-clock" aria-hidden="true"></i>'),
    ("🗓️", '<i class="fa-regular fa-calendar-days" aria-hidden="true"></i>'),
    ("🗓",  '<i class="fa-regular fa-calendar-days" aria-hidden="true"></i>'),
    ("📝", '<i class="fa-solid fa-note-sticky" aria-hidden="true"></i>'),
    ("🔗", '<i class="fa-solid fa-link" aria-hidden="true"></i>'),
    ("ℹ️", '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>'),
    ("ℹ",  '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>'),
    ("✔️", '<i class="fa-solid fa-check" aria-hidden="true"></i>'),
    ("✔",  '<i class="fa-solid fa-check" aria-hidden="true"></i>'),
    ("✓",  '<i class="fa-solid fa-check" aria-hidden="true"></i>'),
    ("✕",  '<i class="fa-solid fa-xmark" aria-hidden="true"></i>'),
    ("✖️", '<i class="fa-solid fa-xmark" aria-hidden="true"></i>'),
    ("✖",  '<i class="fa-solid fa-xmark" aria-hidden="true"></i>'),
    # Toast icons — keep as text
    # ("✓",  "✓"),  # already above
]

replaced_count = 0
for emoji, fa_tag in ICON_MAP:
    n = content.count(emoji)
    if n > 0:
        content = content.replace(emoji, fa_tag)
        replaced_count += n
        print(f"  {emoji} → FA ({n} ocorrências)")

print(f"✓ {replaced_count} emojis substituídos por ícones FA")

# ── 7. Corrigir o login (fake → Supabase real) ───────────────────
OLD_SUBMIT = "form.addEventListener('submit', (e) => {"
NEW_SUBMIT = "form.addEventListener('submit', async (e) => {"

LOGIN_FAKE = (
    "// Simulação de autenticação — substituir por chamada real ao backend"
)

if OLD_SUBMIT in content and LOGIN_FAKE in content:
    content = content.replace(OLD_SUBMIT, NEW_SUBMIT, 1)

    OLD_BLOCK = re.search(
        r"// Simulação de autenticação.*?}, 900\);",
        content, re.DOTALL
    )
    if OLD_BLOCK:
        NEW_BLOCK = """try {
                const authResult = await SupabaseClient.auth.login(user, pass);
                try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (_) {}
                submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';
                setTimeout(() => {
                    hideScreen(false);
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
            } finally {
                setBusy(false);
            }"""
        content = content[:OLD_BLOCK.start()] + NEW_BLOCK + content[OLD_BLOCK.end():]
        print("✓ Login fake substituído por Supabase auth")

# ── 8. Salvar ────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n✅ CONCLUÍDO → {DEST}")
print(f"   Tamanho: {len(content):,} chars")
