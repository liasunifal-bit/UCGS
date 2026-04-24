import os
import re

def fix_icons(file_path):
    # Mapping of sections to icons
    # We look for specific containers and replace their broken content with Lucide tags
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Search Bar Icon
    # Looking for: <span class="search-icon">...</span>
    content = re.sub(
        r'(<span class="search-icon">).*?(</span>)', 
        r'\1<i data-lucide="search" style="width:18px;height:18px;"></i>\2', 
        content
    )

    # 2. Alert Icons (Mapa de Risco, Acidentes, Vacinacao)
    # We'll use a more surgical approach by looking for the alert titles next to the icons
    
    # Mapa de Risco -> Map
    content = re.sub(
        r'(<div class="alert-icon warning">).*?(</div>\s*<div class="alert-content">\s*<div class="alert-title">REVER MAPA DE RISCO)',
        r'\1<i data-lucide="map"></i>\2',
        content,
        flags=re.DOTALL
    )

    # Acidentes (Perfurocortantes) -> Scissors (matches the "knife" look in the 2nd image)
    content = re.sub(
        r'(<div class="alert-icon warning">).*?(</div>\s*<div class="alert-content">\s*<div class="alert-title">REVER PROTOCOLO DE ACIDENTES COM PERFUROCORTANTES)',
        r'\1<i data-lucide="scissors"></i>\2',
        content,
        flags=re.DOTALL
    )

    # Vacinacao -> Syringe
    content = re.sub(
        r'(<div class="alert-icon info">).*?(</div>\s*<div class="alert-content">\s*<div class="alert-title">REVER VACINAÇÃO)',
        r'\1<i data-lucide="syringe"></i>\2',
        content,
        flags=re.DOTALL
    )

    # 3. Sidebar icons (if they are using the same broken pattern)
    # We'll replace common ones based on data-section
    icon_map = {
        'painel': 'layout-dashboard',
        'pacientes': 'users',
        'enfermagem': 'activity',
        'nutricao': 'apple',
        'fisioterapia': 'accessibility',
        'odontologia': 'smile',
        'psicologia': 'brain',
        'seguranca': 'shield-check',
        'protocolos-acidentes': 'alert-octagon',
        'vacinacao': 'syringe'
    }

    for section, icon in icon_map.items():
        # Pattern: <div class="nav-item" data-section="section"> ... <div class="nav-icon">...</div>
        pattern = fr'(<div class="nav-item" data-section="{section}">\s*<div class="nav-icon">).*?(</div>)'
        replacement = fr'\1<i data-lucide="{icon}"></i>\2'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 4. Other stats cards
    # Mapas de Risco Ativos card
    content = re.sub(
        r'(<div class="stat-icon" style="background: #E0F2FE; color: #0EA5E9;">).*?(</div>\s*<span class="stat-label">Mapas de Risco Ativos)',
        r'\1<i data-lucide="map"></i>\2',
        content,
        flags=re.DOTALL
    )
    
    # Protocolos Cadastrados card
    content = re.sub(
        r'(<div class="stat-icon" style="background: #ECFDF5; color: #10B981;">).*?(</div>\s*<span class="stat-label">Protocolos Cadastrados)',
        r'\1<i data-lucide="file-text"></i>\2',
        content,
        flags=re.DOTALL
    )
    
    # Vacinação em Dia card
    content = re.sub(
        r'(<div class="stat-icon" style="background: #FEFCE8; color: #EAB308;">).*?(</div>\s*<span class="stat-label">Vacinação em Dia)',
        r'\1<i data-lucide="syringe"></i>\2',
        content,
        flags=re.DOTALL
    )
    
    # Acidentes Este Mês card
    content = re.sub(
        r'(<div class="stat-icon" style="background: #FFF1F2; color: #E11D48;">).*?(</div>\s*<span class="stat-label">Acidentes Este Mês)',
        r'\1<i data-lucide="alert-triangle"></i>\2',
        content,
        flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Icons fixed in {file_path}")

if __name__ == "__main__":
    target = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML'
    fix_icons(target)
