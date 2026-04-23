"""
CBCJ 2026 — Gerador de Slides PPTX
Panorama da ATJ no Brasil: Distribuição Regional e Evolução Temporal

DADOS REAIS: DataSUS/SIHAS | Procedimento 0408050063
Período: Jan/2015–Jan/2025 | Total: 79.692 AIH aprovadas

Instale: pip install python-pptx
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ─────────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent          # pasta raiz do skill
GRAPH_DIR  = BASE_DIR                               # gráficos ficam na raiz
OUTPUT     = BASE_DIR / "cbcj2026_slides.pptx"

# Slides widescreen 16:9
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ─────────────────────────────────────────────
# PALETA (idêntica aos gráficos)
# ─────────────────────────────────────────────
AZUL_SBCJ    = RGBColor(0x1A, 0x3A, 0x5C)
AZUL_MEDIO   = RGBColor(0x2E, 0x6D, 0xA4)
AZUL_CLARO   = RGBColor(0xA8, 0xC8, 0xE8)
VERDE        = RGBColor(0x2E, 0x8B, 0x57)
VERMELHO     = RGBColor(0xC0, 0x39, 0x2B)
CINZA        = RGBColor(0x7F, 0x8C, 0x8D)
BRANCO       = RGBColor(0xFF, 0xFF, 0xFF)
CINZA_CLARO  = RGBColor(0xF5, 0xF6, 0xFA)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def set_bg(slide, color: RGBColor = None, hex_str: str = "#FFFFFF"):
    """Define cor de fundo do slide."""
    from pptx.oxml.ns import qn
    from lxml import etree
    if color is None:
        r, g, b = int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)
        color = RGBColor(r, g, b)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color: RGBColor, line_color=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # MSO_SHAPE_TYPE.RECTANGLE
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=None, align=PP_ALIGN.LEFT,
             font_name="Calibri", italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font_name
    if color:
        run.font.color.rgb = color
    return txBox


def add_image_centered(slide, img_path, left, top, width, height):
    """Insere imagem mantendo proporção dentro do box."""
    from PIL import Image as PILImage
    img = PILImage.open(img_path)
    iw, ih = img.size
    ratio = min(width / iw, height / ih)
    new_w = int(iw * ratio)
    new_h = int(ih * ratio)
    # Centralizar
    off_x = (width - new_w) // 2
    off_y = (height - new_h) // 2
    slide.shapes.add_picture(
        str(img_path),
        left + off_x, top + off_y,
        new_w, new_h
    )


# ─────────────────────────────────────────────
# SLIDE 1 — CAPA
# ─────────────────────────────────────────────

def slide_capa(prs):
    layout = prs.slide_layouts[6]  # blank
    sl = prs.slides.add_slide(layout)
    set_bg(sl, AZUL_SBCJ)

    # Faixa decorativa inferior
    add_rect(sl,
             Inches(0), SLIDE_H - Inches(1.1),
             SLIDE_W, Inches(1.1),
             RGBColor(0x12, 0x28, 0x40))

    # Linha de acento
    add_rect(sl,
             Inches(0), Inches(2.5),
             SLIDE_W, Inches(0.06),
             AZUL_CLARO)

    # Título principal
    add_text(sl,
             "Panorama da Artroplastia Total do Joelho (ATJ) no SUS",
             Inches(0.8), Inches(1.1),
             Inches(11.7), Inches(1.2),
             font_size=32, bold=True, color=BRANCO,
             align=PP_ALIGN.CENTER)

    # Subtítulo
    add_text(sl,
             "Distribuição Regional e Evolução Temporal (Jan/2015–Jan/2025)",
             Inches(0.8), Inches(2.6),
             Inches(11.7), Inches(0.7),
             font_size=20, color=AZUL_CLARO,
             align=PP_ALIGN.CENTER)

    # Autores (placeholder)
    add_text(sl,
             "Autores: [Inserir nomes] | Instituição: [Inserir] | CBCJ 2026",
             Inches(0.8), Inches(3.5),
             Inches(11.7), Inches(0.6),
             font_size=14, color=BRANCO, align=PP_ALIGN.CENTER, italic=True)

    # Métricas destaque — 3 boxes
    boxes = [
        ("79.692", "AIH aprovadas\n(jan/2015–jan/2025)"),
        ("−52,9%", "Queda COVID-19\n(2019→2020)"),
        ("+57,0%", "Crescimento 2024\nvs. pré-pandemia"),
    ]
    box_w = Inches(3.5)
    box_h = Inches(1.5)
    gap   = Inches(0.35)
    total_w = 3 * box_w + 2 * gap
    start_x = (SLIDE_W - total_w) / 2

    for i, (valor, label) in enumerate(boxes):
        bx = start_x + i * (box_w + gap)
        by = Inches(4.6)
        add_rect(sl, bx, by, box_w, box_h, RGBColor(0x12, 0x28, 0x40))
        add_text(sl, valor,
                 bx, by + Inches(0.12),
                 box_w, Inches(0.65),
                 font_size=28, bold=True, color=AZUL_CLARO,
                 align=PP_ALIGN.CENTER)
        add_text(sl, label,
                 bx, by + Inches(0.75),
                 box_w, Inches(0.65),
                 font_size=11, color=BRANCO,
                 align=PP_ALIGN.CENTER)

    # Rodapé
    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | Consultado: Mar/2026",
             Inches(0.5), SLIDE_H - Inches(0.8),
             Inches(12.3), Inches(0.45),
             font_size=9, color=CINZA, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────
# SLIDE 2 — INTRODUÇÃO / JUSTIFICATIVA
# ─────────────────────────────────────────────

def slide_introducao(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl, CINZA_CLARO)

    # Cabeçalho
    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.1), AZUL_SBCJ)
    add_text(sl, "Introdução & Justificativa",
             Inches(0.5), Inches(0.15),
             Inches(12), Inches(0.8),
             font_size=26, bold=True, color=BRANCO)

    # Linha acento
    add_rect(sl, Inches(0.5), Inches(1.25), Inches(0.06), Inches(4.8), AZUL_MEDIO)

    pontos = [
        ("Contexto", "A osteoartrite é a doença musculoesquelética mais prevalente no mundo, "
         "com impacto crescente no sistema público de saúde brasileiro."),
        ("ATJ no SUS", "A Artroplastia Total do Joelho (proc. 0408050063) é o procedimento "
         "cirúrgico eletivo de maior volume entre cirurgias ortopédicas de grande porte no SUS."),
        ("Lacuna de dados", "Análises epidemiológicas nacionais sobre tendência temporal e distribuição "
         "regional das ATJs são escassas na literatura brasileira."),
        ("Objetivo", "Descrever a distribuição regional e a evolução temporal das ATJs realizadas "
         "pelo SUS no período jan/2015–jan/2025, com ênfase no impacto da pandemia de COVID-19."),
    ]

    y = Inches(1.35)
    for titulo, texto in pontos:
        add_text(sl, titulo,
                 Inches(0.75), y,
                 Inches(11.8), Inches(0.35),
                 font_size=14, bold=True, color=AZUL_SBCJ)
        add_text(sl, texto,
                 Inches(0.75), y + Inches(0.33),
                 Inches(11.8), Inches(0.6),
                 font_size=12, color=RGBColor(0x22, 0x22, 0x22))
        y += Inches(1.1)

    # Rodapé
    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | N=79.692 AIH (jan/2015–jan/2025)",
             Inches(0.5), SLIDE_H - Inches(0.4),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 3 — MÉTODOS
# ─────────────────────────────────────────────

def slide_metodos(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl, CINZA_CLARO)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.1), AZUL_SBCJ)
    add_text(sl, "Métodos",
             Inches(0.5), Inches(0.15),
             Inches(12), Inches(0.8),
             font_size=26, bold=True, color=BRANCO)

    items = [
        ("Delineamento", "Estudo ecológico descritivo, análise de banco de dados secundários."),
        ("Fonte de dados", "Sistema de Informações Hospitalares (SIH/SIHAS) — TabNet/DataSUS."),
        ("Procedimento", "Código 0408050063: Artroplastia Total Primária do Joelho."),
        ("Período", "Janeiro de 2015 a Janeiro de 2025 (N = 79.692 AIH aprovadas).\n"
                    "Nota: 2025 corresponde apenas ao mês de janeiro (dado parcial)."),
        ("Variáveis", "Ano de competência, macrorregião geográfica (5 regiões IBGE), "
                      "total de AIH aprovadas por período."),
        ("Análise", "Análise descritiva com cálculo de percentuais, variação relativa, "
                    "e visualização por gráficos de barras e série temporal (Python 3/Matplotlib)."),
        ("Ética", "Dados agregados e anonimizados de domínio público — dispensada avaliação pelo CEP."),
    ]

    y = Inches(1.25)
    for campo, valor in items:
        # Campo em azul
        add_text(sl, f"▸  {campo}:",
                 Inches(0.6), y,
                 Inches(3.0), Inches(0.38),
                 font_size=12, bold=True, color=AZUL_MEDIO)
        # Valor
        add_text(sl, valor,
                 Inches(3.5), y,
                 Inches(9.3), Inches(0.45),
                 font_size=12, color=RGBColor(0x22, 0x22, 0x22))
        # Separador
        add_rect(sl, Inches(0.6), y + Inches(0.48),
                 Inches(12.1), Inches(0.008), AZUL_CLARO)
        y += Inches(0.72)

    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | Consultado: Março/2026",
             Inches(0.5), SLIDE_H - Inches(0.4),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 4 — GRÁFICO 1: Distribuição Regional
# ─────────────────────────────────────────────

def slide_grafico1(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.0), AZUL_SBCJ)
    add_text(sl, "Resultados — Distribuição Regional das ATJs no SUS (2015–2024)",
             Inches(0.5), Inches(0.12),
             Inches(12.3), Inches(0.78),
             font_size=22, bold=True, color=BRANCO)

    img_path = GRAPH_DIR / "grafico1_distribuicao_regional.png"
    if img_path.exists():
        add_image_centered(sl, img_path,
                           Inches(0.3), Inches(1.05),
                           Inches(8.5), Emu(int(SLIDE_H) - Inches(1.5)))

    # Painel de destaques numéricos
    add_rect(sl, Inches(8.9), Inches(1.1), Inches(4.1), Inches(5.55),
             RGBColor(0xF0, 0xF4, 0xF8))

    add_text(sl, "Destaques",
             Inches(9.0), Inches(1.15),
             Inches(3.8), Inches(0.45),
             font_size=14, bold=True, color=AZUL_SBCJ)

    destaques = [
        ("Sudeste", "57,5%", "45.826 AIH", AZUL_SBCJ),
        ("Sul", "28,7%", "22.873 AIH", AZUL_MEDIO),
        ("Nordeste", "7,9%", "6.313 AIH", CINZA),
        ("Centro-Oeste", "4,4%", "3.531 AIH", CINZA),
        ("Norte", "1,5%", "1.180 AIH", CINZA),
    ]

    dy = Inches(1.7)
    for regiao, pct, abs_val, cor in destaques:
        add_rect(sl, Inches(9.0), dy, Inches(3.8), Inches(0.75), cor)
        add_text(sl, regiao,
                 Inches(9.05), dy + Inches(0.04),
                 Inches(2.0), Inches(0.35),
                 font_size=11, bold=True, color=BRANCO)
        add_text(sl, pct,
                 Inches(11.0), dy + Inches(0.04),
                 Inches(0.9), Inches(0.35),
                 font_size=14, bold=True, color=BRANCO, align=PP_ALIGN.RIGHT)
        add_text(sl, abs_val,
                 Inches(9.05), dy + Inches(0.40),
                 Inches(3.5), Inches(0.28),
                 font_size=9, color=AZUL_CLARO)
        dy += Inches(0.85)

    add_text(sl,
             "Sudeste+Sul concentram 86,2% das ATJs realizadas no SUS",
             Inches(8.9), dy + Inches(0.1),
             Inches(4.1), Inches(0.55),
             font_size=10, bold=True, color=VERMELHO, align=PP_ALIGN.CENTER)

    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | N=79.692",
             Inches(0.5), SLIDE_H - Inches(0.38),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 5 — GRÁFICO 2: Série Temporal
# ─────────────────────────────────────────────

def slide_grafico2(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.0), AZUL_SBCJ)
    add_text(sl, "Resultados — Evolução Temporal das ATJs no SUS (Jan/2015–Jan/2025)",
             Inches(0.5), Inches(0.12),
             Inches(12.3), Inches(0.78),
             font_size=22, bold=True, color=BRANCO)

    img_path = GRAPH_DIR / "grafico2_serie_temporal.png"
    if img_path.exists():
        add_image_centered(sl, img_path,
                           Inches(0.3), Inches(1.05),
                           Inches(9.0), Emu(int(SLIDE_H) - Inches(1.5)))

    # Painel lateral
    add_rect(sl, Inches(9.45), Inches(1.1), Inches(3.55), Inches(5.55),
             RGBColor(0xF0, 0xF4, 0xF8))

    add_text(sl, "Marcos-chave",
             Inches(9.55), Inches(1.2),
             Inches(3.3), Inches(0.4),
             font_size=14, bold=True, color=AZUL_SBCJ)

    marcos = [
        (AZUL_MEDIO,  "2015–2019", "Crescimento contínuo\n7.076 → 8.586 AIH/ano"),
        (VERMELHO,    "2020",      "Colapso COVID-19\n−52,9%: 4.041 AIH\n(mínimo histórico)"),
        (CINZA,       "2021",      "Estagnação\n4.052 AIH\n(ainda em pandemia)"),
        (AZUL_MEDIO,  "2022–2024", "Recuperação acelerada\n8.715 → 13.480 AIH"),
        (VERDE,       "2024",      "Recorde absoluto\n+57,0% vs. 2019\n+28,4% vs. 2023"),
    ]

    dy = Inches(1.75)
    for cor, ano, texto in marcos:
        add_rect(sl, Inches(9.55), dy, Inches(0.06), Inches(0.75), cor)
        add_text(sl, ano,
                 Inches(9.7), dy,
                 Inches(3.1), Inches(0.28),
                 font_size=11, bold=True, color=cor)
        add_text(sl, texto,
                 Inches(9.7), dy + Inches(0.27),
                 Inches(3.1), Inches(0.5),
                 font_size=9, color=RGBColor(0x33, 0x33, 0x33))
        dy += Inches(0.95)

    add_text(sl,
             "* Jan/2025: dado parcial (1 mês apenas)",
             Inches(9.55), dy + Inches(0.1),
             Inches(3.3), Inches(0.35),
             font_size=8, color=CINZA, italic=True)

    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | N=79.692",
             Inches(0.5), SLIDE_H - Inches(0.38),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 6 — GRÁFICO 3: Iniquidade Regional
# ─────────────────────────────────────────────

def slide_grafico3(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.0), AZUL_SBCJ)
    add_text(sl, "Resultados — Iniquidade Regional no Acesso à ATJ pelo SUS",
             Inches(0.5), Inches(0.12),
             Inches(12.3), Inches(0.78),
             font_size=22, bold=True, color=BRANCO)

    img_path = GRAPH_DIR / "grafico3_iniquidade_regional.png"
    if img_path.exists():
        add_image_centered(sl, img_path,
                           Inches(0.3), Inches(1.05),
                           Inches(8.5), Emu(int(SLIDE_H) - Inches(1.5)))

    # Painel
    add_rect(sl, Inches(8.9), Inches(1.1), Inches(4.1), Inches(5.55),
             RGBColor(0xF0, 0xF4, 0xF8))

    add_text(sl, "Iniquidade Regional",
             Inches(9.0), Inches(1.18),
             Inches(3.8), Inches(0.4),
             font_size=14, bold=True, color=AZUL_SBCJ)

    pontos_ineq = [
        ("86,2% das ATJs",
         "concentradas em apenas\nSudeste + Sul"),
        ("13,8% restantes",
         "para Nordeste, Centro-Oeste\ne Norte (>50% da população)"),
        ("Norte: 1,5%",
         "região com maior\ndeficiência de acesso"),
        ("Relação Sudeste/Norte",
         "≈ 39:1 em volume absoluto\nde procedimentos"),
    ]

    dy = Inches(1.7)
    for titulo, desc in pontos_ineq:
        add_rect(sl, Inches(9.0), dy, Inches(3.8), Inches(1.1), BRANCO)
        add_rect(sl, Inches(9.0), dy, Inches(0.08), Inches(1.1), VERMELHO)
        add_text(sl, titulo,
                 Inches(9.15), dy + Inches(0.06),
                 Inches(3.6), Inches(0.38),
                 font_size=11, bold=True, color=AZUL_SBCJ)
        add_text(sl, desc,
                 Inches(9.15), dy + Inches(0.44),
                 Inches(3.6), Inches(0.55),
                 font_size=10, color=RGBColor(0x33, 0x33, 0x33))
        dy += Inches(1.2)

    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | N=79.692",
             Inches(0.5), SLIDE_H - Inches(0.38),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 7 — DISCUSSÃO & CONCLUSÕES
# ─────────────────────────────────────────────

def slide_conclusoes(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl, CINZA_CLARO)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.0), AZUL_SBCJ)
    add_text(sl, "Discussão & Conclusões",
             Inches(0.5), Inches(0.12),
             Inches(12.3), Inches(0.78),
             font_size=26, bold=True, color=BRANCO)

    # Duas colunas
    col_w = Inches(5.9)
    col_gap = Inches(0.5)

    # COLUNA ESQUERDA — Discussão
    add_rect(sl, Inches(0.4), Inches(1.15), col_w, Inches(5.2),
             RGBColor(0xEB, 0xF2, 0xFA))
    add_text(sl, "Discussão",
             Inches(0.55), Inches(1.22),
             col_w - Inches(0.2), Inches(0.4),
             font_size=15, bold=True, color=AZUL_SBCJ)
    add_rect(sl, Inches(0.55), Inches(1.62),
             col_w - Inches(0.2), Inches(0.04), AZUL_MEDIO)

    disc = [
        "A queda de 52,9% em 2020 reflete o impacto direto das medidas de contenção da pandemia sobre cirurgias eletivas.",
        "A recuperação pós-pandemia foi abrupta e acelerada, culminando em recorde histórico em 2024 (+57% vs. 2019), possivelmente impulsionada pela demanda represada.",
        "A concentração de 86,2% dos procedimentos em Sudeste+Sul evidencia marcada iniquidade regional, desproporcionalmente às populações atendidas.",
        "O crescimento sustentado reflete envelhecimento populacional e expansão progressiva da cobertura cirúrgica — tendência que deverá continuar nos próximos anos.",
    ]

    dy = Inches(1.75)
    for txt in disc:
        add_rect(sl, Inches(0.58), dy + Inches(0.08),
                 Inches(0.12), Inches(0.12), AZUL_MEDIO)
        add_text(sl, txt,
                 Inches(0.82), dy,
                 col_w - Inches(0.55), Inches(0.9),
                 font_size=10.5, color=RGBColor(0x22, 0x22, 0x22))
        dy += Inches(1.0)

    # COLUNA DIREITA — Conclusões
    cx = Inches(0.4) + col_w + col_gap
    add_rect(sl, cx, Inches(1.15), col_w, Inches(5.2),
             RGBColor(0xE8, 0xF5, 0xEA))
    add_text(sl, "Conclusões",
             cx + Inches(0.15), Inches(1.22),
             col_w - Inches(0.2), Inches(0.4),
             font_size=15, bold=True, color=VERDE)
    add_rect(sl, cx + Inches(0.15), Inches(1.62),
             col_w - Inches(0.2), Inches(0.04), VERDE)

    concl = [
        "As ATJs no SUS cresceram 90,5% entre 2015 e 2024, demonstrando expansão significativa do acesso.",
        "A pandemia de COVID-19 causou contração histórica (2020), com recuperação total superada em 2022 e recorde em 2024.",
        "A iniquidade regional é crítica: Norte e Nordeste permanecem severamente sub-representados, exigindo políticas públicas de equidade.",
        "Monitoramento contínuo e expansão regional seletiva são essenciais para garantir acesso equânime à ATJ pelo SUS.",
    ]

    dy = Inches(1.75)
    for txt in concl:
        add_rect(sl, cx + Inches(0.18), dy + Inches(0.08),
                 Inches(0.12), Inches(0.12), VERDE)
        add_text(sl, txt,
                 cx + Inches(0.42), dy,
                 col_w - Inches(0.55), Inches(0.9),
                 font_size=10.5, color=RGBColor(0x22, 0x22, 0x22))
        dy += Inches(1.0)

    add_text(sl,
             "Fonte: DataSUS/SIHAS | Proc. 0408050063 | N=79.692 AIH (jan/2015–jan/2025) | Consultado: Mar/2026",
             Inches(0.5), SLIDE_H - Inches(0.38),
             Inches(12.3), Inches(0.35),
             font_size=8, color=CINZA, align=PP_ALIGN.RIGHT)


# ─────────────────────────────────────────────
# SLIDE 8 — REFERÊNCIAS
# ─────────────────────────────────────────────

def slide_referencias(prs):
    layout = prs.slide_layouts[6]
    sl = prs.slides.add_slide(layout)
    set_bg(sl, CINZA_CLARO)

    add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(1.0), AZUL_SBCJ)
    add_text(sl, "Referências",
             Inches(0.5), Inches(0.12),
             Inches(12.3), Inches(0.78),
             font_size=26, bold=True, color=BRANCO)

    refs = [
        "1. DataSUS/SIHAS. Sistema de Informações Hospitalares. Ministério da Saúde. "
        "Disponível em: http://datasus.saude.gov.br. Acesso em: mar. 2026.",

        "2. Ministério da Saúde. SIGTAP — Sistema de Gerenciamento da Tabela de Procedimentos. "
        "Procedimento 0408050063: Artroplastia Total Primária do Joelho.",

        "3. Coimbra IB, et al. Consenso Brasileiro para o Tratamento da Osteoartrite (Artrose). "
        "Rev Bras Reumatol. 2004;44(6):450-9.",

        "4. GBD 2019 Diseases and Injuries Collaborators. Global burden of musculoskeletal disorders. "
        "Lancet. 2020;396(10258):1204-22.",

        "5. Pivec R, et al. Hip and knee arthroplasty. Lancet. 2012;380(9855):1768-77. "
        "doi:10.1016/S0140-6736(12)60607-2.",

        "6. IBGE. Projeções da População Brasileira 2024. Instituto Brasileiro de "
        "Geografia e Estatística. Rio de Janeiro, 2024.",

        "7. ANS. Dados do setor — procedimentos de alta complexidade. "
        "Agência Nacional de Saúde Suplementar, 2024.",
    ]

    y = Inches(1.2)
    for ref in refs:
        add_text(sl, ref,
                 Inches(0.6), y,
                 Inches(12.1), Inches(0.65),
                 font_size=10, color=RGBColor(0x22, 0x22, 0x22))
        y += Inches(0.72)

    add_text(sl,
             "Contato: [e-mail do autor correspondente] | CBCJ 2026",
             Inches(0.5), SLIDE_H - Inches(0.38),
             Inches(12.3), Inches(0.35),
             font_size=9, color=CINZA, align=PP_ALIGN.CENTER, italic=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def gerar_pptx():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H

    print("🔵 Gerando slides PPTX — CBCJ 2026\n")

    slide_capa(prs);       print("✅ Slide 1: Capa")
    slide_introducao(prs); print("✅ Slide 2: Introdução")
    slide_metodos(prs);    print("✅ Slide 3: Métodos")
    slide_grafico1(prs);   print("✅ Slide 4: Gráfico 1 — Distribuição Regional")
    slide_grafico2(prs);   print("✅ Slide 5: Gráfico 2 — Série Temporal")
    slide_grafico3(prs);   print("✅ Slide 6: Gráfico 3 — Iniquidade Regional")
    slide_conclusoes(prs); print("✅ Slide 7: Discussão & Conclusões")
    slide_referencias(prs);print("✅ Slide 8: Referências")

    prs.save(str(OUTPUT))
    print(f"\n🎉 Arquivo salvo em: {OUTPUT}")
    print(f"   {OUTPUT.stat().st_size // 1024} KB | 8 slides | 16:9 widescreen")


if __name__ == "__main__":
    gerar_pptx()
