import re

def fix_html_encoding(filepath):
    # Lendo o arquivo (tentando utf-8 primeiro)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Garantir que <meta charset="UTF-8"> esta no topo do <head>
    if '<meta charset="UTF-8">' not in content:
        content = re.sub(r'(<head.*?>)', r'\1\n    <meta charset="UTF-8">', content, count=1, flags=re.IGNORECASE)

    # Adicionar FontAwesome no head
    fa_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">'
    if fa_link not in content:
        content = re.sub(r'(<head.*?>)', r'\1\n    ' + fa_link, content, count=1, flags=re.IGNORECASE)

    # Mapeamento de emojis conhecidos (em caracteres utf-8 e tambem seus codigos)
    # A base e o que a usuaria mandou, mais alguns encontrados no arquivo.
    replacements = {
        '📊': '&#x1F4CA;',
        '👥': '&#x1F465;',
        '📋': '&#x1F4CB;',
        '🗺️': '&#x1F5FA;',
        '🗺': '&#x1F5FA;',
        '📑': '&#x1F4D1;',
        '💉': '&#x1F489;',
        '🧪': '&#x1F9EA;',
        '⚠️': '&#x26A0;',
        '🩺': '&#x1FA7A;',
        '🥦': '&#x1F966;',
        '🧑': '&#x1F9D1;',
        '🏋️': '&#x1F3CB;',
        '🏋': '&#x1F3CB;',
        '🦷': '&#x1F9B7;',
        '🧠': '&#x1F9E0;',
        '📞': '&#x1F4DE;',
        '🔔': '&#x1F514;',
        '🚨': '&#x1F6A8;',
        '🔍': '&#x1F50D;',
        '➕': '&#x2795;',
        '📅': '&#x1F4C5;',
        '🚪': '&#x1F6AA;',
        '📷': '&#x1F4F7;',
        '👤': '&#x1F464;',
        '📈': '&#x1F4C8;',
        '🔪': '&#x1F52A;',
        '🥗': '&#x1F957;',
        '🪪': '&#x1FAAA;',
        '🌓': '&#x1F317;',
        '🔧': '&#x1F527;',
        '🎯': '&#x1F3AF;',
        '🦴': '&#x1F9B4;',
        '🔬': '&#x1F52C;',
        '💡': '&#x1F4A1;',
        '⚕️': '&#x2695;',
        '⚕': '&#x2695;',
        '✅': '&#x2705;',
        '❌': '&#x274C;',
        '✏️': '&#x270F;',
        '✏': '&#x270F;',
        '🗑️': '&#x1F5D1;',
        '🗑': '&#x1F5D1;'
    }

    # Fazer a substituicao
    for emoji, entity in replacements.items():
        content = content.replace(emoji, entity)

    # Tambem procurar por caracteres corrompidos que possam ter ficado no utf-8 (mojibake duplo)
    # Por exemplo: 'Gestão' se tornou 'Gesto' mas com utf-8 errors='replace' vira 'Gesto'
    # Melhor nao arriscar corromper palavras normais, focar apenas nos emojis solicitados.

    # Salvar o arquivo forcando utf-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fix applied successfully to " + filepath)

fix_html_encoding('site nevo.HTML')
