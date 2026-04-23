import re

f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
f.close()

def replace_emoji(match):
    s = match.group(0)
    try:
        # Codificamos a string literal para bytes usando cp1252
        # (isso reverte a interpretacao errada como cp1252 de volta aos bytes originais do utf-8)
        b = s.encode('cp1252')
        # E decodificamos esses bytes originais de volta pra string real utf-8
        decoded = b.decode('utf-8')
        
        # Como o html precisa de compatibilidade garantida, geramos a entidade &#x...;
        out = ''
        for c in decoded:
            if ord(c) > 0x1000: # emojis e caracteres especiais
                out += f'&#x{ord(c):X};'
            else:
                out += c
        return out
    except:
        return s

# A expressao regular procura pelo \u00f0 (ð) seguido do \u0178 (Ÿ) e mais 2 a 10 caracteres
# que compoem o restante do emoji em bytes interpretados como cp1252.
fixed_content = re.sub(r'\u00f0\u0178[^\s<"\']{0,10}', replace_emoji, content)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Done")
