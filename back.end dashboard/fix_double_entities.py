import re
import html

f=open('site nevo.HTML', 'r', encoding='utf-8')
content=f.read()
f.close()

def replace_mojibake_entities(match):
    s = match.group(0)
    # Primeiro resolvemos as entidades HTML de volta para os caracteres corrompidos
    unescaped = html.unescape(s)
    try:
        # Codificamos como latin1 (que eh byte a byte 0-255)
        # O cp1252 falha em alguns bytes como 0x81, 0x8D, etc. O latin1 mapeia 1:1.
        b = unescaped.encode('latin1')
        # E decodificamos como utf-8
        decoded = b.decode('utf-8')
        
        # Agora pegamos o emoji e transformamos em html entity novamente, mas O CERTO!
        out = ''
        for c in decoded:
            if ord(c) > 0x00FF:
                out += f'&#x{ord(c):X};'
            else:
                out += c
        return out
    except Exception as e:
        # Se nao for possivel, retorna original
        return s

# Regex procura o \u00f0 (ð) seguido de caracteres HTML entity &#x...; ou texto normal
# Na verdade, a sequencia eh \u00f0 seguido de &#x[0-9A-F]+; repetido ate 4 vezes.
# Mas tb podem ter outros caracteres corrompidos q ficaram abaixo de 0x0100 (ex: \x8D, \x9D etc) 
# q nao viraram &#x; Entao vamos apenas procurar a string desescapada que comeca com ð
fixed_content = re.sub(r'\u00f0(?:&#x[0-9A-F]+;|[^\s<]){1,6}', replace_mojibake_entities, content, flags=re.IGNORECASE)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Double encoded entities fixed!")
