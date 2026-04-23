#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCGS – Substituição DIRETA dos padrões corrompidos no sidebar.
Em vez de tentar reverter o encoding, mapeamos cada sequência
corrompida específica diretamente para a tag Lucide correspondente.
"""
import re

DEST = "site nevo.HTML"

with open(DEST, "r", encoding="utf-8") as f:
    content = f.read()

# Mapeamento DIRETO: sequência corrompida → tag Lucide
# Estes são os padrões exatos que aparecem no arquivo (verificados acima)
DIRECT_MAP = [
    # ðŸ"Š = 📊 (bar chart)
    ('ðŸ"Š',  '<i data-lucide="bar-chart-3"></i>'),
    # ðŸ'¤ = 👤 (user)
    ('ðŸ\'¤',  '<i data-lucide="user"></i>'),
    # ðŸ"‹ = 📋 (clipboard-list)
    ('ðŸ"‹',  '<i data-lucide="clipboard-list"></i>'),
    # ðŸ—º️ = 🗺️ (map)
    ('ðŸ—º\ufe0f', '<i data-lucide="map"></i>'),
    ('ðŸ—º',  '<i data-lucide="map"></i>'),
    # ðŸ"§ = 🔧 (wrench)
    ('ðŸ"§',  '<i data-lucide="wrench"></i>'),
    # ðŸ'‰ = 💉 (syringe)
    ('ðŸ\'‰',  '<i data-lucide="syringe"></i>'),
    # ðŸ"¬ = 🔬 (microscope)
    ('ðŸ"¬',  '<i data-lucide="microscope"></i>'),
    # âš ️ = ⚠️ (triangle-alert)
    ('â\x9a \ufe0f', '<i data-lucide="triangle-alert"></i>'),
    ('â\x9a ',  '<i data-lucide="triangle-alert"></i>'),
    # ðŸ¥ = 🏥 (hospital)
    ('ðŸ¥',   '<i data-lucide="hospital"></i>'),
    # ðŸ¥— = 🥗 (salad)
    ('ðŸ¥—',  '<i data-lucide="salad"></i>'),
    # ðŸ©º = 🩺 (stethoscope)
    ('ðŸ©º',  '<i data-lucide="stethoscope"></i>'),
    # ðŸ¦´ = 🦴 (bone)
    ('ðŸ¦´',  '<i data-lucide="bone"></i>'),
    # ðŸ¦· = 🦷 (tooth)
    ('ðŸ¦·',  '<i data-lucide="sparkles"></i>'),
    # ðŸ§  = 🧠 (brain)
    ('ðŸ§\u0080',  '<i data-lucide="brain"></i>'),
    # ðŸ"ž = 📞 (phone)
    ('ðŸ"ž',  '<i data-lucide="phone"></i>'),
    # ðŸ"ˆ = 📈 (trending-up)
    ('ðŸ"ˆ',  '<i data-lucide="trending-up"></i>'),
    # ðŸ"‰ = 📉 (trending-down)
    ('ðŸ"‰',  '<i data-lucide="trending-down"></i>'),
    # âš™ï¸ / âš™ = ⚙️ (settings)
    ('â\x9a™\ufe0f', '<i data-lucide="settings"></i>'),
    ('â\x9a™',  '<i data-lucide="settings"></i>'),
    # ðŸ"… = 📅 (calendar)
    ('ðŸ"…',  '<i data-lucide="calendar"></i>'),
    # ðŸ"" = 🔔 (bell)
    ('ðŸ""',  '<i data-lucide="bell"></i>'),
    # ðŸŒ" = 🌓 (moon)
    ('ðŸŒ"',  '<i data-lucide="circle-half-stroke"></i>'),
    # ðŸŒ™ = 🌙 (moon)
    ('ðŸŒ™',  '<i data-lucide="moon"></i>'),
    # â˜€ï¸ / â˜€ = ☀️ (sun)
    ('â˜\u0080\ufe0f', '<i data-lucide="sun"></i>'),
    ('â˜\u0080',  '<i data-lucide="sun"></i>'),
    # ðŸšª = 🚪 (log-out)
    ('ðŸšª',  '<i data-lucide="log-out"></i>'),
    # âœ‰ = ✉ (mail)
    ('â\x9c‰',  '<i data-lucide="mail"></i>'),
    # ðŸŠ = 🪪 (id-card)
    ('ðŸŠ',  '<i data-lucide="id-card"></i>'),
    # âœ… = ✅ (circle-check)
    ('â\x9c…',  '<i data-lucide="circle-check"></i>'),
    # âŒ› = ⌛ (hourglass)
    ('â\x8c›',  '<i data-lucide="hourglass"></i>'),
    # â³ = ⏳ (hourglass)
    ('â³',   '<i data-lucide="hourglass"></i>'),
    # ðŸš¨ = 🚨 (siren)
    ('ðŸš¨',  '<i data-lucide="siren"></i>'),
    # ðŸ'Š = 💊 (pill)
    ('ðŸ\'Š',  '<i data-lucide="pill"></i>'),
    # â¤ï¸ / â¤ = ❤️ (heart)
    ('â\x9d¤\ufe0f', '<i data-lucide="heart"></i>'),
    ('â\x9d¤',  '<i data-lucide="heart"></i>'),
    # ðŸ'ª = 💪 (dumbbell)
    ('ðŸ\'ª',  '<i data-lucide="dumbbell"></i>'),
    # â„ï¸ / â„ = ❄️ (snowflake)
    ('â\x9d„\ufe0f', '<i data-lucide="snowflake"></i>'),
    ('â\x9d„',  '<i data-lucide="snowflake"></i>'),
    # ðŸ"Ž = 📎 (paperclip)
    ('ðŸ"Ž',  '<i data-lucide="paperclip"></i>'),
    # ðŸŽ¯ = 🎯 (target)
    ('ðŸŽ¯',  '<i data-lucide="target"></i>'),
    # âš¡ = ⚡ (zap)
    ('â\x9a¡',  '<i data-lucide="zap"></i>'),
    # ðŸ" = 📐 (ruler)
    ('ðŸ"',   '<i data-lucide="ruler"></i>'),
    # ðŸ§® = 🧮 (calculator)
    ('ðŸ§®',  '<i data-lucide="calculator"></i>'),
    # ðŸš« = 🚫 (ban)
    ('ðŸš«',  '<i data-lucide="ban"></i>'),
    # âœï¸ / â  = ✏️ (pen-line)
    ('â\x9c\ufe0f', '<i data-lucide="pen-line"></i>'),
    ('â\x9c',  '<i data-lucide="pen-line"></i>'),
    # ðŸ"„ = 📄 (file-text)
    ('ðŸ"„',  '<i data-lucide="file-text"></i>'),
    # ðŸ'¾ = 💾 (save)
    ('ðŸ\'¾',  '<i data-lucide="save"></i>'),
    # ðŸ—'ï¸ / ðŸ—' = 🗑️ (trash-2)
    ('ðŸ—\'\\ufe0f', '<i data-lucide="trash-2"></i>'),
    ('ðŸ—\'',  '<i data-lucide="trash-2"></i>'),
    # âž• = ➕ (plus)
    ('â\x9e•',  '<i data-lucide="plus"></i>'),
    # âž– = ➖ (minus)
    ('â\x9e–',  '<i data-lucide="minus"></i>'),
    # ðŸ"„ = 🔄 (rotate-cw) — cuidado com colisão com 📄
    # Nota: 🔄 (U+1F504) e 📄 (U+1F4C4) têm bytes diferentes
    # ðŸ"¥ = 📥 (download)
    ('ðŸ"¥',  '<i data-lucide="download"></i>'),
    # â„¹ = ℹ (info)
    ('â„¹',  '<i data-lucide="info"></i>'),
    # ðŸ·ï¸ / ðŸ· = 🏷️ (tag)
    ('ðŸ·\ufe0f', '<i data-lucide="tag"></i>'),
    ('ðŸ·',   '<i data-lucide="tag"></i>'),
    # ðŸ"ª = 🔪 (flame)
    ('ðŸ"ª',  '<i data-lucide="flame"></i>'),
    # ðŸ§ª = 🧪 (flask)
    ('ðŸ§ª',  '<i data-lucide="flask-conical"></i>'),
    # ðŸ'‡ = 💇? or outros - skip para não corromper mais
]

replaced_count = 0
for seq, tag in DIRECT_MAP:
    n = content.count(seq)
    if n > 0:
        content = content.replace(seq, tag)
        replaced_count += n
        print(f"  [{n}x] {repr(seq[:10])} → {tag[:40]}")

print(f"\nTotal: {replaced_count} sequências substituídas")

with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[OK] Salvo.")
