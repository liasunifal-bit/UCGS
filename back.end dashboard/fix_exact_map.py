#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCGS – Substituição PRECISA baseada nos bytes reais extraídos do arquivo.
Usa os codepoints Unicode exatos de cada sequência corrompida.
"""

DEST = "site nevo.HTML"

with open(DEST, "r", encoding="utf-8") as f:
    content = f.read()

# Mapeamento EXATO: string corrompida (codepoints reais) → tag Lucide
# Baseado na análise dos bytes reais do arquivo
EXACT_MAP = [
    # [0] ðŸ"Š = 📊 bar-chart-3
    ('\u00f0\u0178\u201c\u0160',  '<i data-lucide="bar-chart-3"></i>'),
    # [1] ðŸ'¤ = 👤 user
    ('\u00f0\u0178\u2018\u00a4',  '<i data-lucide="user"></i>'),
    # [2] ðŸ"‹ = 📋 clipboard-list  (também [16] duplicate)
    ('\u00f0\u0178\u201c\u2039',  '<i data-lucide="clipboard-list"></i>'),
    # [3] ðŸ—º️ = 🗺️ map
    ('\u00f0\u0178\u2014\u00ba\ufe0f', '<i data-lucide="map"></i>'),
    ('\u00f0\u0178\u2014\u00ba',       '<i data-lucide="map"></i>'),
    # [4] ðŸ"§ = 🔧 wrench
    ('\u00f0\u0178\u201d\u00a7',  '<i data-lucide="wrench"></i>'),
    # [5] ðŸ'‰ = 💉 syringe
    ('\u00f0\u0178\u2019\u2030',  '<i data-lucide="syringe"></i>'),
    # [6] ðŸ"¬ = 🔬 microscope
    ('\u00f0\u0178\u201d\u00ac',  '<i data-lucide="microscope"></i>'),
    # [7] âš ️ = ⚠️ triangle-alert
    ('\u00e2\u0161\u00a0\ufe0f',  '<i data-lucide="triangle-alert"></i>'),
    ('\u00e2\u0161\u00a0',        '<i data-lucide="triangle-alert"></i>'),
    # [8] ðŸ\x8f¥ = 🏥 hospital
    ('\u00f0\u0178\u008f\u00a5',  '<i data-lucide="hospital"></i>'),
    # [9] ðŸ¥— = 🥗 salad
    ('\u00f0\u0178\u00a5\u2014',  '<i data-lucide="salad"></i>'),
    # [10] ðŸ©º = 🩺 stethoscope
    ('\u00f0\u0178\u00a9\u00ba',  '<i data-lucide="stethoscope"></i>'),
    # [11] ðŸ¦´ = 🦴 bone
    ('\u00f0\u0178\u00a6\u00b4',  '<i data-lucide="bone"></i>'),
    # [12] ðŸ¦· = 🦷 tooth/sparkles
    ('\u00f0\u0178\u00a6\u00b7',  '<i data-lucide="sparkles"></i>'),
    # [13] ðŸ§ = 🧠 brain (only 3 chars – brain partial)
    ('\u00f0\u0178\u00a7',        '<i data-lucide="brain"></i>'),
    # [14] ðŸ"ž = 📞 phone
    ('\u00f0\u0178\u201c\u017e',  '<i data-lucide="phone"></i>'),
    # [15] ðŸ"ˆ = 📈 trending-up
    ('\u00f0\u0178\u201c\u02c6',  '<i data-lucide="trending-up"></i>'),
    # [17] âš™️ = ⚙️ settings
    ('\u00e2\u0161\u2122\ufe0f',  '<i data-lucide="settings"></i>'),
    ('\u00e2\u0161\u2122',        '<i data-lucide="settings"></i>'),
    # Extras comuns que podem aparecer em outras seções
    # ðŸ"‰ = 📉 trending-down
    ('\u00f0\u0178\u201c\u2030',  '<i data-lucide="trending-down"></i>'),
    # ðŸ"… = 📅 calendar
    ('\u00f0\u0178\u201c\u2026',  '<i data-lucide="calendar"></i>'),
    # ðŸ"" = 🔔 bell
    ('\u00f0\u0178\u201d\u201c',  '<i data-lucide="bell"></i>'),
    # ðŸŒ™ = 🌙 moon
    ('\u00f0\u0178\u0152\u2122',  '<i data-lucide="moon"></i>'),
    # ðŸšª = 🚪 log-out
    ('\u00f0\u0178\u0161\u00aa',  '<i data-lucide="log-out"></i>'),
    # âœ… = ✅ circle-check
    ('\u00e2\u009c\u2026',        '<i data-lucide="circle-check"></i>'),
    # â³ = ⏳ hourglass
    ('\u00e2\u00b3',              '<i data-lucide="hourglass"></i>'),
    # ðŸš¨ = 🚨 siren
    ('\u00f0\u0178\u0161\u00a8',  '<i data-lucide="siren"></i>'),
    # ðŸ'Š = 💊 pill
    ('\u00f0\u0178\u2019\u008a',  '<i data-lucide="pill"></i>'),
    # â¤ï¸ = ❤️ heart
    ('\u00e2\u009d\u00a4\ufe0f',  '<i data-lucide="heart"></i>'),
    ('\u00e2\u009d\u00a4',        '<i data-lucide="heart"></i>'),
    # ðŸ'ª = 💪 dumbbell
    ('\u00f0\u0178\u2019\u00aa',  '<i data-lucide="dumbbell"></i>'),
    # â„ï¸ = ❄️ snowflake
    ('\u00e2\u009d\u201e\ufe0f',  '<i data-lucide="snowflake"></i>'),
    ('\u00e2\u009d\u201e',        '<i data-lucide="snowflake"></i>'),
    # ðŸ"Ž = 📎 paperclip
    ('\u00f0\u0178\u201c\u017d',  '<i data-lucide="paperclip"></i>'),
    # ðŸŽ¯ = 🎯 target
    ('\u00f0\u0178\u017d\u00af',  '<i data-lucide="target"></i>'),
    # âš¡ = ⚡ zap
    ('\u00e2\u0161\u00a1',        '<i data-lucide="zap"></i>'),
    # ðŸ§® = 🧮 calculator
    ('\u00f0\u0178\u00a7\u00ae',  '<i data-lucide="calculator"></i>'),
    # ðŸš« = 🚫 ban
    ('\u00f0\u0178\u0161\u00ab',  '<i data-lucide="ban"></i>'),
    # ðŸ"„ = 📄 file-text
    ('\u00f0\u0178\u201c\u201e',  '<i data-lucide="file-text"></i>'),
    # ðŸ'¾ = 💾 save
    ('\u00f0\u0178\u2019\u00be',  '<i data-lucide="save"></i>'),
    # ðŸ—' = 🗑️ trash-2
    ('\u00f0\u0178\u2014\u2018\ufe0f', '<i data-lucide="trash-2"></i>'),
    ('\u00f0\u0178\u2014\u2018',       '<i data-lucide="trash-2"></i>'),
    # âž• = ➕ plus
    ('\u00e2\u009e\u2022',        '<i data-lucide="plus"></i>'),
    # ðŸ"¥ = 📥 download
    ('\u00f0\u0178\u201d\u00a5',  '<i data-lucide="download"></i>'),
    # â„¹ = ℹ info
    ('\u00e2\u201e\u00b9',        '<i data-lucide="info"></i>'),
    # ðŸ"Ž extra search icon
    ('\u00f0\u0178\u201d\u008e',  '<i data-lucide="search"></i>'),
    # ðŸ"± = 📱 smartphone
    ('\u00f0\u0178\u201d\u00b1',  '<i data-lucide="smartphone"></i>'),
    # âœ" = ✓ check mark (keep as text for toasts)
    # ('\u00e2\u009c\u201c', '✓'),
    # âœ• = ✕ x mark (keep as text for toasts)
    # ('\u00e2\u009c\u2022', '✕'),
]

replaced_count = 0
for seq, tag in EXACT_MAP:
    n = content.count(seq)
    if n > 0:
        content = content.replace(seq, tag)
        replaced_count += n
        print(f"  [{n}x] {repr(seq)[:30]} → {tag[:50]}")

print(f"\nTotal substituído: {replaced_count} ocorrências")

with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[OK] Arquivo salvo ({len(content):,} chars)")
