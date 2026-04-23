f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
f.close()

original_len = len(content)
out = []
for c in content:
    # 0x0100 to 0x10FFFF includes all non-latin characters, emojis, symbols, etc.
    # Excludes 0x00-0xFF which is ASCII + Latin-1 (so 'ã', 'ç', 'é' stay as literal utf-8 characters)
    if ord(c) > 0x00FF:
        out.append(f'&#x{ord(c):X};')
    else:
        out.append(c)

fixed_content = ''.join(out)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Modificacoes feitas. Diff length: {len(fixed_content) - original_len}")
