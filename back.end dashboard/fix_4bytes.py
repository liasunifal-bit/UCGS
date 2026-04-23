import re

f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
f.close()

# Encontrar todas as moedas de caracteres que começam com \u00f0 (ð)
# Emojis em utf-8 comecam com F0 9F. Entao \u00f0\u009f.
def replace_emoji(match):
    s = match.group(0)
    try:
        b = s.encode('latin1')
        decoded = b.decode('utf-8')
        if any(ord(c) > 0x2000 for c in decoded):
            out = ''
            for c in decoded:
                if ord(c) > 0x2000:
                    out += f'&#x{ord(c):X};'
                else:
                    out += c
            return out
    except:
        pass
    return s

# Regex para pegar sequencias de 4 caracteres na faixa 0x80-0xFF
# A maioria dos emojis no Supabase/UCGS usa 4 bytes.
fixed_content = re.sub(r'[\u0080-\u00FF]{4}', replace_emoji, content)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Done")
