#!/usr/bin/env python3
"""
Gerador de PNG da Agenda Liga LIAS.
Edite a seção # === DADOS === antes de executar.
"""

import base64, os, sys
from pathlib import Path

# =====================================================================
# === DADOS — edite aqui antes de executar ============================
# =====================================================================

SEMANA        = "30 de março a 10 de abril de 2026"
LOGO_PATH     = ""   # caminho para o .jpeg/.png da logo (deixe "" para usar SVG fallback)
OUTPUT_PATH   = r"c:\Users\maria\Downloads\antigravity lias\agenda_liga_lias.png"

# Lista de eventos para "Datas importantes"
# Cada dict: dia (int), mes (str), titulo, horario, modalidade, tags (list[str])
EVENTOS = [
    {
        "dia": 3,
        "mes": "ABR",
        "cor": "verde",
        "titulo": 'Post de atualizações: "News IA"',
        "horario": "Sexta-feira",
        "modalidade": "online",
        "tags": ["Divulgação", "News IA"],
        "tags_cor": ["verde", "teal"],
    },
    {
        "dia": 4,
        "mes": "ABR",
        "cor": "azul",
        "titulo": "Postagem do Podcast",
        "horario": "Sábado - Canal Oficial",
        "modalidade": "online",
        "tags": ["Podcast", "Midia"],
        "tags_cor": ["azul", "teal"],
    },
    {
        "dia": 6,
        "mes": "ABR",
        "cor": "verde",
        "titulo": "Desenvolvimento de Projetos (Coordenadores)",
        "horario": "Segunda-feira - Início das atividades",
        "modalidade": "presencial/hibrido",
        "tags": ["Grupos de Estudos", "Manus", "Z.Ai"],
        "tags_cor": ["verde", "teal", "teal"],
    },
    {
        "dia": 10,
        "mes": "ABR",
        "cor": "azul",
        "titulo": "Reunião Geral da Liga",
        "horario": "Sexta-feira - 17h",
        "modalidade": "presencial",
        "tags": ["Geral", "Síncrona"],
        "tags_cor": ["azul", "verde"],
    },
]

# Cards do Instagram — deixe lista vazia [] para omitir a seção
INSTAGRAM = [
    {"dia_semana": "Segundas-feiras", "cor": "verde", "titulo": 'Pôster "Aprendendo a IA"', "desc": "Conteúdo educativo semanal"},
    {"dia_semana": "Sextas-feiras",   "cor": "azul",  "titulo": 'Pôster "News IA"',          "desc": "Novidades da semana em IA"},
]

# Informação para os ligantes — deixe "" para omitir a seção
INFO_LIGANTES = "Todas as tarefas da semana já estão no site da liga."
INFO_LIGANTES_SUB = "Acesse o site e confira suas responsabilidades desta semana."

# Calendário — defina os 7 dias da semana (seg→dom) e quais têm destaque
# formato: lista de dicts com "num" (int), "fds" (bool), "destaque" (bool), "label" (str ou "")
# Calendário — defina os 14 dias (2 semanas seg→dom)
CALENDARIO = [
    {"num": 30, "fds": False, "destaque": False, "label": ""},
    {"num": 31, "fds": False, "destaque": False, "label": ""},
    {"num": 1,  "fds": False, "destaque": False, "label": ""},
    {"num": 2,  "fds": False, "destaque": False, "label": ""},
    {"num": 3,  "fds": False, "destaque": True,  "label": "News"},
    {"num": 4,  "fds": True,  "destaque": True,  "label": "Pod"},
    {"num": 5,  "fds": True,  "destaque": False, "label": ""},
    
    {"num": 6,  "fds": False, "destaque": True,  "label": "Proj"},
    {"num": 7,  "fds": False, "destaque": False, "label": ""},
    {"num": 8,  "fds": False, "destaque": False, "label": ""},
    {"num": 9,  "fds": False, "destaque": False, "label": ""},
    {"num": 10, "fds": False, "destaque": True,  "label": "Reu"},
    {"num": 11, "fds": True,  "destaque": False, "label": ""},
    {"num": 12, "fds": True,  "destaque": False, "label": ""},
]

# =====================================================================
# === TEMPLATE HTML ===================================================
# =====================================================================

SVG_FALLBACK = """<svg viewBox='0 0 88 88' xmlns='http://www.w3.org/2000/svg' width='88' height='88'>
  <circle cx='44' cy='44' r='44' fill='#0d2535'/>
  <ellipse cx='36' cy='34' rx='13' ry='16' fill='#1D9E75' opacity='.9' transform='rotate(-20 36 34)'/>
  <ellipse cx='52' cy='34' rx='13' ry='16' fill='#2a8ab8' opacity='.9' transform='rotate(20 52 34)'/>
  <ellipse cx='36' cy='54' rx='13' ry='16' fill='#1a7a8a' opacity='.9' transform='rotate(20 36 54)'/>
  <ellipse cx='52' cy='54' rx='13' ry='16' fill='#1a5a8a' opacity='.9' transform='rotate(-20 52 54)'/>
  <rect x='38' y='39' width='12' height='12' rx='2' fill='#e0f4f8' stroke='#7ab8c8' stroke-width='.5'/>
  <rect x='41' y='42' width='6' height='6' rx='1' fill='#1a3a50'/>
  <rect x='49' y='31' width='8' height='3' rx='1' fill='white'/>
  <rect x='52' y='28' width='3' height='8' rx='1' fill='white'/>
  <path d='M33 51 Q29 55 31 58' fill='none' stroke='white' stroke-width='1.5' stroke-linecap='round'/>
  <circle cx='31' cy='59' r='2' fill='none' stroke='white' stroke-width='1'/>
  <path d='M51 53 Q49 51 47 53 Q45 55 47 58 L51 61 L55 58 Q57 55 55 53 Q53 51 51 53Z' fill='white' opacity='.9'/>
</svg>"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Inter:wght@300;400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a1520;display:flex;justify-content:center;padding:40px;font-family:'Inter',sans-serif}
.card{width:800px;background:linear-gradient(160deg,#0d2535 0%,#0a1e2c 60%,#091828 100%);border-radius:24px;overflow:hidden;border:1px solid #1e4a5e;position:relative}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#1D9E75,#2a8ab8,#1D9E75)}
.header{padding:32px 40px 24px;display:flex;align-items:center;gap:24px;border-bottom:1px solid #1a3a4e}
.logo-wrap{flex-shrink:0;width:92px;height:92px;border-radius:50%;border:2px solid #2a6a80;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#0d2535}
.logo-wrap img{width:88px;height:88px;object-fit:contain;border-radius:50%}
.header-text h1{font-family:'Montserrat',sans-serif;font-size:28px;font-weight:800;color:#d8f0ea;letter-spacing:-.5px;line-height:1.1}
.header-text h1 span{color:#1D9E75}
.header-text .sub{font-size:12px;color:#5a9aaa;margin-top:6px;letter-spacing:.3px}
.header-text .semana{display:inline-block;margin-top:10px;background:#0F6E56;color:#9FE1CB;font-size:11px;font-weight:700;padding:4px 14px;border-radius:20px;font-family:'Montserrat',sans-serif;letter-spacing:.5px}
.body{padding:28px 40px 32px;display:flex;flex-direction:column;gap:24px}
.section-label{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.section-label .bar{width:4px;height:18px;background:#1D9E75;border-radius:2px}
.section-label .bar.blue{background:#2a8ab8}
.section-label span{font-family:'Montserrat',sans-serif;font-size:11px;font-weight:700;color:#1D9E75;letter-spacing:1.5px;text-transform:uppercase}
.section-label span.blue{color:#4ab0d0}
.eventos{display:flex;flex-direction:column;gap:10px}
.evento-card{background:#112a3a;border:1px solid #1e4a5e;border-radius:12px;padding:14px 18px;display:flex;align-items:flex-start;gap:16px}
.evento-date{flex-shrink:0;background:#0F6E56;border-radius:10px;padding:8px 14px;text-align:center;min-width:60px}
.evento-date.azul{background:#185FA5}
.evento-date .day{font-family:'Montserrat',sans-serif;font-size:20px;font-weight:800;color:#c0ede0;line-height:1}
.evento-date.azul .day{color:#c0e4f8}
.evento-date .month{font-size:10px;font-weight:700;color:#5DCAA5;letter-spacing:.5px;margin-top:3px;font-family:'Montserrat',sans-serif}
.evento-date.azul .month{color:#5ab0d8}
.evento-info h3{font-family:'Montserrat',sans-serif;font-size:14px;font-weight:700;color:#d8f0ea;margin-bottom:4px}
.evento-info .meta{font-size:12px;color:#5a9aaa;margin-bottom:8px}
.evento-info .tags{display:flex;gap:6px;flex-wrap:wrap}
.tag{background:#0F6E56;color:#9FE1CB;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;font-family:'Montserrat',sans-serif;letter-spacing:.3px}
.tag.azul{background:#185FA5;color:#a0d4f0}
.tag.teal{background:#0a3a4a;color:#5ab8d0;border:1px solid #1e5a6e}
.insta-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.insta-card{background:#112a3a;border:1px solid #1e4a5e;border-radius:12px;padding:16px}
.insta-card.verde{border-left:3px solid #1D9E75}
.insta-card.azul{border-left:3px solid #2a8ab8}
.insta-day{font-family:'Montserrat',sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}
.insta-card.verde .insta-day{color:#1D9E75}
.insta-card.azul .insta-day{color:#2a8ab8}
.insta-title{font-family:'Montserrat',sans-serif;font-size:13px;font-weight:700;color:#d8f0ea;margin-bottom:4px}
.insta-desc{font-size:11px;color:#5a9aaa}
.info-card{background:#112a3a;border:1px solid #1e4a5e;border-left:3px solid #1D9E75;border-radius:12px;padding:14px 18px;display:flex;align-items:center;gap:14px}
.info-icon{width:36px;height:36px;background:#0F6E56;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Montserrat',sans-serif;font-size:16px;font-weight:800;color:#9FE1CB;flex-shrink:0}
.info-card p{font-size:12.5px;color:#a0c8c0;line-height:1.5}
.info-card p strong{color:#d8f0ea;font-weight:600}
.calendario{background:#112a3a;border:1px solid #1e4a5e;border-radius:12px;padding:16px 12px 14px}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}
.cal-header{font-size:10px;font-weight:700;color:#3a8a9a;letter-spacing:.5px;text-transform:uppercase;padding-bottom:8px;font-family:'Montserrat',sans-serif}
.cal-day{font-size:16px;font-weight:500;color:#4a8a9a;padding:8px 4px;border-radius:8px;font-family:'Montserrat',sans-serif}
.cal-day.fds{color:#2a5a6a}
.cal-destaque-wrap{display:flex;flex-direction:column;align-items:center}
.cal-day.destaque{background:#1D9E75;color:white;font-weight:800;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto;font-size:16px}
.cal-label{font-size:9px;color:#5DCAA5;font-weight:700;letter-spacing:.5px;margin-top:3px;font-family:'Montserrat',sans-serif}
.footer{background:#091828;border-top:1px solid #1a3a4e;padding:14px 40px;display:flex;align-items:center;justify-content:space-between}
.footer p{font-size:11px;color:#3a6a7a}
.footer p span{color:#1D9E75;font-weight:600}
.footer-bar{height:4px;background:linear-gradient(90deg,#1D9E75,#2a8ab8,#1D9E75)}
"""

# =====================================================================
# === BUILDERS ========================================================
# =====================================================================

def build_logo(logo_path):
    if logo_path and Path(logo_path).exists():
        ext = Path(logo_path).suffix.lower().replace(".", "")
        mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/{mime};base64,{b64}" alt="Logo Liga LIAS"/>'
    else:
        return SVG_FALLBACK

def build_evento(ev):
    cor_date = "azul" if ev["cor"] == "azul" else ""
    tags_html = ""
    for t, tc in zip(ev.get("tags", []), ev.get("tags_cor", [])):
        tags_html += f'<span class="tag {tc}">{t}</span>'
    return f"""
    <div class="evento-card">
      <div class="evento-date {cor_date}">
        <div class="day">{ev['dia']}</div>
        <div class="month">{ev['mes']}</div>
      </div>
      <div class="evento-info">
        <h3>{ev['titulo']}</h3>
        <p class="meta">Horário: {ev['horario']} &nbsp;•&nbsp; Modalidade: {ev['modalidade']}</p>
        <div class="tags">{tags_html}</div>
      </div>
    </div>"""

def build_instagram(cards):
    if not cards:
        return ""
    items = "".join(f"""
    <div class="insta-card {c['cor']}">
      <div class="insta-day">{c['dia_semana']}</div>
      <div class="insta-title">{c['titulo']}</div>
      <div class="insta-desc">{c['desc']}</div>
    </div>""" for c in cards)
    return f"""
    <div>
      <div class="section-label"><div class="bar blue"></div><span class="blue">Divulgação no Instagram</span></div>
      <div class="insta-grid">{items}</div>
    </div>"""

def build_info(msg, sub):
    if not msg:
        return ""
    return f"""
    <div>
      <div class="section-label"><div class="bar"></div><span>Informações para os ligantes</span></div>
      <div class="info-card">
        <div class="info-icon">i</div>
        <p><strong>{msg}</strong><br>{sub}</p>
      </div>
    </div>"""

def build_calendario(dias):
    HEADERS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    headers = "".join(f'<div class="cal-header">{h}</div>' for h in HEADERS)
    cells = ""
    for d in dias:
        if d["destaque"]:
            label = f'<div class="cal-label">{d["label"]}</div>' if d["label"] else ""
            cells += f'<div class="cal-destaque-wrap"><div class="cal-day destaque">{d["num"]}</div>{label}</div>'
        else:
            fds_cls = " fds" if d["fds"] else ""
            cells += f'<div class="cal-day{fds_cls}">{d["num"]}</div>'
    return f"""
    <div>
      <div class="section-label"><div class="bar"></div><span>Visão da semana</span></div>
      <div class="calendario">
        <div class="cal-grid">{headers}{cells}</div>
      </div>
    </div>"""

def build_html(semana, logo_path, eventos, instagram, info_msg, info_sub, calendario):
    logo_html   = build_logo(logo_path)
    eventos_html = "".join(build_evento(e) for e in eventos)
    insta_html  = build_instagram(instagram)
    info_html   = build_info(info_msg, info_sub)
    cal_html    = build_calendario(calendario)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="logo-wrap">{logo_html}</div>
    <div class="header-text">
      <h1>Agenda <span>Liga LIAS</span></h1>
      <p class="sub">Liga de Inteligência Artificial na Saúde &nbsp;•&nbsp; UNIFAL-MG</p>
      <span class="semana">Semana {semana}</span>
    </div>
  </div>
  <div class="body">
    <div>
      <div class="section-label"><div class="bar"></div><span>Datas importantes</span></div>
      <div class="eventos">{eventos_html}</div>
    </div>
    {insta_html}
    {info_html}
    {cal_html}
  </div>
  <div class="footer">
    <p>Liga de <span>Inteligência Artificial na Saúde</span></p>
    <p>UNIFAL-MG &nbsp;•&nbsp; 2025</p>
  </div>
  <div class="footer-bar"></div>
</div>
</body>
</html>"""

# =====================================================================
# === MAIN ============================================================
# =====================================================================

def main():
    import os

    html = build_html(
        semana      = SEMANA,
        logo_path   = LOGO_PATH,
        eventos     = EVENTOS,
        instagram   = INSTAGRAM,
        info_msg    = INFO_LIGANTES,
        info_sub    = INFO_LIGANTES_SUB,
        calendario  = CALENDARIO,
    )

    html_path = r"c:\Users\maria\Downloads\antigravity lias\.agent\skills\agenda-liga-lias\scripts\agenda_render.html"
    with open(html_path, "w") as f:
        f.write(html)

    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 880, "height": 900})
        page.set_content(html, wait_until="networkidle")
        page.wait_for_timeout(2000)
        page.locator(".card").screenshot(path=OUTPUT_PATH, type="png")
        browser.close()

    print(f"✅ PNG gerado: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")

if __name__ == "__main__":
    main()
