import shutil

chars = 'áãâàéêíóõôúçÁÃÉÊÍÓÔÚÇ°ºª—–‘’“”→'
mapping = {}
for c in chars:
    try:
        bad = c.encode('utf-8').decode('cp1252')
        mapping[bad] = c
    except:
        pass

shutil.copy('site nevo_backup.HTML', 'site nevo.HTML')

with open('site nevo.HTML', 'r', encoding='utf-8') as f:
    text = f.read()

for bad, good in mapping.items():
    text = text.replace(bad, good)

# Also fix the emojis we know are broken
# 📊 U+1F4CA \xf0\x9f\x93\x8a -> ðŸ“Š
text = text.replace('ðŸ“Š', '📊')
# ⚡ U+26A1 \xe2\x9a\xa1 -> âš¡
text = text.replace('âš¡', '⚡')
# ⚠️ U+26A0 \xe2\x9a\xa0 -> âš
text = text.replace('âš\xa0', '⚠️')

with open('site nevo.HTML', 'w', encoding='utf-8') as f:
    f.write(text)

print('Restored and fixed mapping!')
