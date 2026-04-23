import re
import html

f=open('site nevo.HTML', 'r', encoding='utf-8')
content=f.read()
f.close()

# Dicionario de fallback para os bytes cp1252 que viraram unicode no html
# Exemplo: &#x178; eh Ÿ (U+0178) que em cp1252 eh 0x9F
cp1252_to_byte = {
    0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
    0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
    0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
    0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
    0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F
}

def decode_mojibake(s):
    # s eh string como: ð&#x178;&#x2014;
    unescaped = html.unescape(s)
    b = bytearray()
    for c in unescaped:
        o = ord(c)
        if o in cp1252_to_byte:
            b.append(cp1252_to_byte[o])
        elif o <= 0xFF:
            b.append(o)
        else:
            # Caractere desconhecido
            b.append(0x3F) # ?
            
    try:
        decoded = b.decode('utf-8')
        out = ''
        for c in decoded:
            out += f'&#x{ord(c):X};'
        return out
    except:
        return s

# Procurar o \u00f0 seguido de entidades 
fixed_content = re.sub(r'\u00f0(?:&#x[0-9A-F]+;)+', lambda m: decode_mojibake(m.group(0)), content, flags=re.IGNORECASE)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed the remaining double encoded mojibake!")
