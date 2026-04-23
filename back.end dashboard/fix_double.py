import re
import html

with open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Primeiro, reverte todas as entidades HTML seguras que criamos
content = html.unescape(content)

# Funcao para reverter dupla codificacao
def fix_double_encoding(match):
    s = match.group(0)
    try:
        # A string "Ã£" vira bytes b'\xc3\xa3', que decodificado em utf-8 vira "ã"
        return s.encode('latin1').decode('utf-8')
    except Exception as e:
        return s

# Procura por qualquer sequencia que pareca UTF-8 lido como Latin1
# Caracteres de inicio UTF-8: \xC2 a \xDF (2 bytes), \xE0 a \xEF (3 bytes), \xF0 a \xF4 (4 bytes)
# Seguidos por bytes de continuacao: \x80 a \xBF
pattern = r'[\xc2-\xdf][\x80-\xbf] | [\xe0-\xef][\x80-\xbf]{2} | [\xf0-\xf4][\x80-\xbf]{3}'
# Na verdade, eh mais simples usar uma expressao regular unificada, sem espacos:
pattern = r'[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xf4][\x80-\xbf]{3}'

fixed_content = re.sub(pattern, fix_double_encoding, content)

# Para garantir que nunca mais quebre, vamos reconverter TUDO que for > 127 para HTML Entity novamente
out = []
for c in fixed_content:
    if ord(c) > 127:
        out.append(f'&#x{ord(c):X};')
    else:
        out.append(c)

final_html = ''.join(out)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Double encoding fix applied successfully!")
