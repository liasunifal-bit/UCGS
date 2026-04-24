import os
import re

def polish_and_shine(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up broken comment decorations
    # Use re.escape or avoid regex for simple strings
    content = content.replace('ââ€¢Â ', '= ')
    content = content.replace('???', '---')

    # 2. Fix missed Lucide icons in specific classes
    # Magnifying glass in ex-autocomplete and similar
    content = re.sub(
        r'<span class="ex-autocomplete-icon".*?>.*?</span>',
        r'<span class="ex-autocomplete-icon" aria-hidden="true"><i data-lucide="search" style="width:14px;height:14px;"></i></span>',
        content
    )
    content = re.sub(
        r'<span class="ex-search-icon".*?>.*?</span>',
        r'<span class="ex-search-icon" aria-hidden="true"><i data-lucide="search" style="width:14px;height:14px;"></i></span>',
        content
    )

    # 3. Fix Protocol icons
    content = re.sub(
        r'(<div class="protocol-icon".*?>).*?(</div>)',
        r'\1<i data-lucide="file-text"></i>\2',
        content
    )

    # 4. Fix Nutrition Nav icons
    content = re.sub(
        r'(<span class="nut-nav-icon">).*?(</span>)',
        r'\1<i data-lucide="activity" style="width:16px;height:16px;"></i>\2',
        content
    )

    # 5. Fix specific section titles with broken chars
    replacements_manual = {
        'Avaliaao': 'Avaliação',
        'Antropomtrica': 'Antropométrica',
        'Plano Alimentar': 'Plano Alimentar',
        'Preferncias': 'Preferências',
        'Observaes': 'Observações',
        'Almoo': 'Almoço',
        'Manh': 'Manhã',
        'Ceia': 'Ceia'
    }
    for old, new in replacements_manual.items():
        content = content.replace(old, new)
    
    # 6. Fix stat icons
    content = re.sub(
        r'(<div class="nut-kpi-icon".*?>).*?(</div>)',
        r'\1<i data-lucide="trending-up"></i>\2',
        content
    )
    content = re.sub(
        r'(<div class="pe-stat-icon".*?>).*?(</div>)',
        r'\1<i data-lucide="activity"></i>\2',
        content
    )

    # 7. Modernize primary button (Plus icon)
    content = re.sub(
        r'<button class="btn-primary".*?>\s*<svg.*?</svg>\s*Novo Mapa\s*</button>',
        r'<button class="btn-primary" onclick="openNovoMapaModal()" style="padding:10px 22px;font-size:0.9rem;border-radius:var(--radius-md);box-shadow:0 4px 14px rgba(14,165,233,0.3);display:inline-flex;align-items:center;gap:8px;white-space:nowrap;"><i data-lucide="plus"></i> Novo Mapa</button>',
        content
    )

    # 8. General cleanup of common words
    replacements_global = {
        'Configuraes': 'Configurações',
        'Notificaes': 'Notificações',
        'Pgina': 'Página',
        'Histrico': 'Histórico',
        'Ateno': 'Atenção',
        'Sade': 'Saúde',
        'Gesto': 'Gestão',
        'Pronturio': 'Prontuário',
        'Usurio': 'Usuário'
    }
    for old, new in replacements_global.items():
        content = content.replace(old, new)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Visual polish complete in {file_path}")

if __name__ == "__main__":
    target = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML'
    polish_and_shine(target)
