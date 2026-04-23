import re
f=open('site nevo.HTML', 'r', encoding='utf-8', errors='ignore')
content=f.read()
if re.search(r'id=[\'\"]login', content, re.IGNORECASE):
    print("HAS LOGIN ID")
else:
    print("NO LOGIN ID")
