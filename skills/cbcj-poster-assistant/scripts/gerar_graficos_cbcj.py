"""
CBCJ 2026 — Gerador de Gráficos para Pôster Eletrônico
Panorama da ATJ no Brasil: Distribuição Regional e Evolução Temporal

DADOS REAIS: DataSUS/SIHAS | Procedimento 0408050063
Período: Jan/2015–Jan/2025 | Total: 79.692 AIH aprovadas
Nota: 2025 corresponde apenas a Janeiro/2025

Instale os pacotes: pip install matplotlib numpy
"""

import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Configurar saída para suportar caracteres Unicode no Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.right'] = False

# ─────────────────────────────────────────────
# PALETA DE CORES (padrão científico/SBCJ)
# ─────────────────────────────────────────────
AZUL_SBCJ    = "#1A3A5C"
AZUL_MEDIO   = "#2E6DA4"
AZUL_CLARO   = "#A8C8E8"
VERDE_ACENTO = "#2E8B57"
VERMELHO     = "#C0392B"
CINZA        = "#7F8C8D"
FUNDO        = "#FFFFFF"

OUTPUT_DIR = ".."

# ─────────────────────────────────────────────
# DADOS REAIS — DataSUS / SIHAS
# Procedimento: 0408050063 – Artroplastia Total Primária do Joelho
# Período: Jan/2015–Jan/2025 | Fonte: TabNet/DataSUS (consultado Mar/2026)
# Nota: valor de 2025 = somente Janeiro/2025 (parcial)
# ─────────────────────────────────────────────
ANOS          = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
PROCEDIMENTOS = [7_076, 7_182, 7_477, 7_649, 8_586, 4_041, 4_052, 8_715, 10_501, 13_480, 933]
TOTAL         = 79_692

# Métricas calculadas automaticamente com dados reais
PICO_PRE_COVID  = 8_586                                                          # 2019
NADIR_COVID     = 4_041                                                          # 2020
QUEDA_PCT       = round((PICO_PRE_COVID - NADIR_COVID) / PICO_PRE_COVID * 100, 1)   # 52,9%
RECORDE_2024    = 13_480
VAR_VS_2019     = round((RECORDE_2024 - PICO_PRE_COVID) / PICO_PRE_COVID * 100, 1)  # +57,0%
VAR_VS_2023     = round((RECORDE_2024 - 10_501) / 10_501 * 100, 1)              # +28,4%

# Distribuição regional (Valores atualizados)
REGIOES   = ["Sudeste", "Sul", "Nordeste", "Centro-\nOeste", "Norte"]
ABSOLUTOS = [45_811, 22_855, 6_316, 3_534, 1_176]
TOTAL     = sum(ABSOLUTOS)
PERCENTS  = [round(a / TOTAL * 100, 2) for a in ABSOLUTOS]


# ═══════════════════════════════════════════════
# GRÁFICO 1 — Distribuição Regional (barras)
# ═══════════════════════════════════════════════
def grafico_distribuicao_regional():
    cores = [AZUL_SBCJ, AZUL_MEDIO, AZUL_CLARO, "#5B9BD5", "#C9DAF0"]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor=FUNDO)
    bars = ax.barh(REGIOES[::-1], PERCENTS[::-1], color=cores[::-1],
                   edgecolor="white", linewidth=1.2, height=0.6)

    for bar, pct, n in zip(bars, PERCENTS[::-1], ABSOLUTOS[::-1]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"  {pct:.2f}%  (n={n:,})",
                va='center', ha='left', fontsize=12,
                fontweight='bold', color=AZUL_SBCJ)

    ax.set_xlabel("Participação no volume nacional (%)", fontsize=12,
                  labelpad=10, color=CINZA)
    ax.set_title(
        f"Distribuição Regional das ATJs no SUS\n"
        f"(2015–2024 | N = {TOTAL:,} AIH aprovadas)",
        fontsize=14, fontweight='bold', color=AZUL_SBCJ, pad=15)
    ax.set_xlim(0, 75)
    ax.tick_params(axis='y', labelsize=12, colors=AZUL_SBCJ)
    ax.tick_params(axis='x', labelsize=10, colors=CINZA)
    ax.axvline(x=0, color=CINZA, linewidth=0.8)

    ax.annotate("86,16% concentrados\nem Sudeste e Sul",
                xy=(57.48, 3.5), xytext=(42, 1.0),
                fontsize=10, color=VERMELHO, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=VERMELHO, lw=1.5))

    ax.text(0.98, 0.02, "Fonte: DataSUS/SIHAS | Proc. 0408050063",
            transform=ax.transAxes, fontsize=7, color=CINZA, ha='right')

    fig.tight_layout()
    path = f"{OUTPUT_DIR}/grafico1_distribuicao_regional.png"
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=FUNDO)
    print(f"[OK] Salvo: {path}")
    plt.close()


# ═══════════════════════════════════════════════
# GRÁFICO 2 — Série Temporal (linha + eventos)
# ═══════════════════════════════════════════════
def grafico_serie_temporal():
    fig, ax = plt.subplots(figsize=(13, 6), facecolor=FUNDO)

    # Área pandêmica
    ax.axvspan(2019.7, 2021.3, alpha=0.07, color=VERMELHO)

    # Linha principal (2015-2024, excluindo jan/2025 parcial)
    ax.plot(ANOS[:-1], PROCEDIMENTOS[:-1], color=AZUL_SBCJ, linewidth=2.8,
            marker='o', markersize=9, markerfacecolor="white",
            markeredgecolor=AZUL_SBCJ, markeredgewidth=2.2, zorder=3)

    # Preenchimento sob a curva (série completa)
    ax.fill_between(ANOS[:-1], PROCEDIMENTOS[:-1], alpha=0.07, color=AZUL_SBCJ)

    # Linha tracejada: 2024 → jan/2025
    ax.plot([2024, 2025], [PROCEDIMENTOS[-2], PROCEDIMENTOS[-1]],
            color=CINZA, linewidth=1.6, linestyle='--', zorder=2)

    # Ponto 2025 diferenciado (dado parcial = apenas janeiro)
    ax.plot(2025, PROCEDIMENTOS[-1], marker='D', markersize=9,
            markerfacecolor=CINZA, markeredgecolor=AZUL_SBCJ,
            markeredgewidth=1.8, zorder=4)

    # Linha de referência pré-pandemia
    ax.axhline(y=PICO_PRE_COVID, color=CINZA, linewidth=1.0,
               linestyle='--', alpha=0.6)

    # Anotação: queda COVID
    ax.annotate(
        f"▼ {QUEDA_PCT}%\n(COVID-19, 2020)",
        xy=(2020, NADIR_COVID), xytext=(2020.15, 6_100),
        fontsize=10, color=VERMELHO, fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=VERMELHO, lw=1.5))

    # Anotação: recorde 2024
    ax.annotate(
        f"Recorde 2024\n+{VAR_VS_2019:.1f}% vs. 2019\n+{VAR_VS_2023:.1f}% vs. 2023",
        xy=(2024, RECORDE_2024), xytext=(2021.8, 12_300),
        fontsize=10, color=VERDE_ACENTO, fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=VERDE_ACENTO, lw=1.5))

    # Anotação: jan/2025 (dado parcial)
    ax.annotate(
        f"Jan/2025\n(n={PROCEDIMENTOS[-1]:,})*",
        xy=(2025, PROCEDIMENTOS[-1]), xytext=(2024.2, 2_500),
        fontsize=9, color=CINZA, fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=CINZA, lw=1.2))

    # Valores sobre cada ponto (exceto 2025 — já anotado)
    for ano, val in zip(ANOS[:-1], PROCEDIMENTOS[:-1]):
        x_off, y_off = 0, 350
        va, ha = 'bottom', 'center'

        if ano == 2019:
            y_off = 700  # Sobe para descolar da linha de referência (8.586)
        elif ano == 2020:
            y_off, va = -650, 'top'
        elif ano == 2021:
            x_off, ha = -0.15, 'right' # Nudge para esquerda para descolar da linha ascendente
        elif ano == 2023:
            x_off, ha = -0.15, 'right' # Move para a esquerda do ponto para não cruzar a linha íngreme
        elif ano == 2024:
            x_off, ha = 0.15, 'left' # Nudge para direita para balancear

        ax.text(ano + x_off, val + y_off, f"{val:,}", ha=ha, va=va,
                fontsize=8.5, color=AZUL_SBCJ, fontweight='bold')

    # Eixo X: últimos rótulo indica dado parcial
    rotulos = [str(a) for a in ANOS[:-1]] + ["Jan\n2025*"]
    ax.set_xticks(ANOS)
    ax.set_xticklabels(rotulos, fontsize=10, color=CINZA)
    ax.set_ylabel("AIH aprovadas", fontsize=12, labelpad=10, color=CINZA)
    ax.set_title(
        "Evolução Temporal das ATJs no SUS (Jan/2015–Jan/2025)\n"
        "Impacto da Pandemia COVID-19 e Recuperação",
        fontsize=14, fontweight='bold', color=AZUL_SBCJ, pad=15)
    ax.set_ylim(0, 15_500)
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.tick_params(axis='y', labelsize=10, colors=CINZA)

    patch_covid = mpatches.Patch(color=VERMELHO, alpha=0.15, label="Período pandêmico")
    linha_ref = plt.Line2D([0], [0], color=CINZA, linestyle='--',
                           label=f"Referência pré-pandemia (2019: {PICO_PRE_COVID:,})")
    ponto_parcial = plt.Line2D([0], [0], marker='D', color='w',
                               markerfacecolor=CINZA, markersize=8,
                               label="* Jan/2025 — dado parcial (1 mês)")
    ax.legend(handles=[patch_covid, linha_ref, ponto_parcial],
              fontsize=9, loc='upper left', framealpha=0.6, edgecolor=CINZA)

    ax.text(0.98, 0.02,
            f"Fonte: DataSUS/SIHAS | Proc. 0408050063 | N={TOTAL:,} (jan/2015–jan/2025)",
            transform=ax.transAxes, fontsize=7, color=CINZA, ha='right')

    fig.tight_layout()
    path = f"{OUTPUT_DIR}/grafico2_serie_temporal.png"
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=FUNDO)
    print(f"[OK] Salvo: {path}")
    plt.close()


# ═══════════════════════════════════════════════
# GRÁFICO 3 — Iniquidade regional
# ═══════════════════════════════════════════════
def grafico_iniquidade():
    grupos  = ["Sudeste + Sul\n(86,16%)", "Nordeste + CO + Norte\n(13,84%)"]
    valores = [86.16, 13.84]
    cores   = [AZUL_SBCJ, AZUL_CLARO]
    explode = (0.04, 0.04)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor=FUNDO)

    # — Pizza —
    wedges, texts, autotexts = axes[0].pie(
        valores, labels=grupos, colors=cores, explode=explode,
        autopct='%1.2f%%', startangle=90,
        textprops={'fontsize': 11, 'color': AZUL_SBCJ},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    for at in autotexts:
        at.set_fontsize(13)
        at.set_fontweight('bold')
        at.set_color('white')
    # Título interno removido

    # — Barras por região —
    regioes_label = ["Sudeste", "Sul", "Nordeste", "Centro-\nOeste", "Norte"]
    bar_cores = [AZUL_SBCJ, AZUL_SBCJ, AZUL_CLARO, AZUL_CLARO, AZUL_CLARO]
    b = axes[1].bar(regioes_label, PERCENTS, color=bar_cores,
                    edgecolor="white", linewidth=1.2, width=0.55)

    for bar, pct, n in zip(b, PERCENTS, ABSOLUTOS):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            f"{pct:.2f}%\n({n:,})", ha='center', va='bottom',
            fontsize=10, fontweight='bold', color=AZUL_SBCJ)

    axes[1].set_ylim(0, 72)
    axes[1].set_ylabel("% do Volume Nacional", fontsize=11, color=CINZA)
    # Título interno removido
    axes[1].tick_params(axis='x', labelsize=10.5, colors=AZUL_SBCJ)
    axes[1].tick_params(axis='y', labelsize=10, colors=CINZA)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    p1 = mpatches.Patch(color=AZUL_SBCJ, label="Maior acesso (SE + S)")
    p2 = mpatches.Patch(color=AZUL_CLARO, label="Menor acesso (N + NE + CO)")
    axes[1].legend(handles=[p1, p2], fontsize=9, loc='upper right',
                   framealpha=0.6, edgecolor=CINZA)

    # Título Principal e Subtítulo Estratégico
    fig.suptitle("Desigualdade no acesso regional à ATJ pelo SUS (2015–2025)",
                 fontsize=15, fontweight='bold', color=AZUL_SBCJ, y=1.05)
    
    fig.text(0.5, 0.97, 
             "Sudeste e Sul concentram a maior parte dos procedimentos, evidenciando desigualdade no acesso entre regiões",
             ha='center', fontsize=11, color=AZUL_SBCJ, fontweight='normal', alpha=0.9)
    fig.tight_layout()
    path = f"{OUTPUT_DIR}/grafico3_iniquidade_regional.png"
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=FUNDO)
    print(f"[OK] Salvo: {path}")
    plt.close()


# ═══════════════════════════════════════════════
# EXECUTAR
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print("[INFO] Gerando graficos CBCJ 2026 - DADOS REAIS DataSUS\n")
    print(f"   Total AIH aprovadas:          {TOTAL:,}")
    print(f"   Queda COVID (2019→2020):      {QUEDA_PCT}%")
    print(f"   Crescimento 2024 vs. 2019:   +{VAR_VS_2019}%")
    print(f"   Crescimento 2024 vs. 2023:   +{VAR_VS_2023}%\n")
    grafico_distribuicao_regional()
    grafico_serie_temporal()
    grafico_iniquidade()
    print(f"\n[DONE] 3 graficos gerados (300 dpi) em: {OUTPUT_DIR}/")
