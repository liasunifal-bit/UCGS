import re

with open('site nevo_backup.HTML', 'r', encoding='utf-8-sig') as f:
    content = f.read()

print("Original:", repr(re.search(r'Gest.{0,10}', content).group(0)))

def fix_double_encoding(match):
    s = match.group(0)
    try:
        return s.encode('latin1').decode('utf-8')
    except Exception as e:
        return s

pattern = r'[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xf4][\x80-\xbf]{3}'
fixed_content = re.sub(pattern, fix_double_encoding, content)

print("Fixed:", repr(re.search(r'Gest.{0,10}', fixed_content).group(0)))

print("Has ''' error?:", "'''" in fixed_content)
