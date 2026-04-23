import re

with open("site nevo.HTML", "r", encoding="utf-8") as f:
    c = f.read()

# Encontra TODA a sidebar HTML
idx = c.find("Menu Principal")
if idx < 0:
    idx = c.find("nav-label")
chunk = c[idx:idx+4000]

# Extrair tudo entre as tags nav-icon
pattern = r'class="nav-icon"[^>]*>([\s\S]*?)</div>'
matches = re.findall(pattern, chunk)

print(f"Encontrados {len(matches)} nav-icon items:")
for i, m in enumerate(matches[:20]):
    stripped = m.strip()
    b = stripped.encode("utf-8")
    print(f"  [{i}] chars={[hex(ord(ch)) for ch in stripped]} bytes={b.hex()} display={repr(stripped)}")
