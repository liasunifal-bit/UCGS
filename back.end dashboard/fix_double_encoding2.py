import re

def fix_double_encoding(text):
    def replace_match(match):
        s = match.group(0)
        try:
            # Tentar converter os caracteres literais usando latin1 que mapeia 1:1
            b = s.encode('latin1')
            decoded = b.decode('utf-8')
            # Se a decodificacao gerou caracteres normais + emojis
            if decoded != s:
                # Retornar html entities para tudo que for emoji
                out = ''
                for c in decoded:
                    if ord(c) > 0x2000: # Qualquer simbolo, emoji, etc
                        out += f'&#x{ord(c):X};'
                    else:
                        out += c
                return out
        except:
            pass
        return s

    # Buscar sequencias de caracteres com acentos (bytes 0x80 a 0xFF no latin1)
    # A regex busca palavras que contem caracteres nao-ascii
    # Mas como podem ter misturas (ex: ðŸ“Š), vamos buscar grupos grandes
    return re.sub(r'[\u0080-\u00FF]+', replace_match, text)

f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
f.close()

original_len = len(content)
fixed_content = fix_double_encoding(content)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Modificacoes feitas. Diff length: {len(fixed_content) - original_len}")
