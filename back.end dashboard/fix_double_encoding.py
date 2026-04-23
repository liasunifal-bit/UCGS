import re

def fix_double_encoding(text):
    def replace_match(match):
        s = match.group(0)
        try:
            # Tentar converter os caracteres literais (que eram cp1252) de volta para bytes, depois para utf-8
            b = s.encode('cp1252')
            decoded = b.decode('utf-8')
            # Se deu certo e tem pelo menos um caractere nao-ascii, usar isso
            if decoded != s:
                # Mas so substituir se for um emoji (ord > 1000) ou algo do tipo
                if any(ord(c) > 0x1F300 for c in decoded):
                    return f'&#x{ord(decoded[0]):X};' # Ou retornar a entidade HTML
                return decoded
        except:
            pass
        return s

    # Buscar sequencias de caracteres com acentos (bytes 0x80 a 0xFF no cp1252)
    # \u0080-\u00FF sao os caracteres do Latin-1/cp1252
    return re.sub(r'[\u0080-\u00FF]+', replace_match, text)

# Testar
f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
f.close()

original_len = len(content)
fixed_content = fix_double_encoding(content)

# Substituir manualmente as entidades como o usuario pediu:
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
    '➕': '&#x2795;'
}
for k, v in replacements.items():
    fixed_content = fixed_content.replace(k, v)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Modificacoes feitas. Diff length: {len(fixed_content) - original_len}")
