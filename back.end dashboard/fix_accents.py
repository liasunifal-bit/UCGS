import re

with open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

out = []
for c in content:
    if ord(c) > 127:
        out.append(f'&#x{ord(c):X};')
    else:
        out.append(c)

final_content = ''.join(out)

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("All non-ASCII characters have been safely converted to HTML entities!")
