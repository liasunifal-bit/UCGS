import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

scripts = []
for m in re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE):
    # m.group(1) is the inner code
    code = m.group(1).strip()
    if code:
        scripts.append({
            'start_line': content.count('\n', 0, m.start()) + 1,
            'end_line': content.count('\n', 0, m.end()) + 1,
            'content': code
        })

print(f"Total scripts: {len(scripts)}")

# For script index 3 (0-based) and 19 (if they match the same array)
try:
    s3 = scripts[3]
    print(f"\n--- SCRIPT 3 (Lines {s3['start_line']} to {s3['end_line']}) ---")
    lines3 = s3['content'].split('\n')
    print("Start:", '\n'.join(lines3[:5]))
    print("...")
    print("End:", '\n'.join(lines3[-10:]))
    
    # Save script 3 to file
    with open('script3.js', 'w', encoding='utf-8') as f:
        f.write(s3['content'])
except Exception as e:
    print("Error getting script 3:", e)

try:
    s19 = scripts[19]
    print(f"\n--- SCRIPT 19 (Lines {s19['start_line']} to {s19['end_line']}) ---")
    lines19 = s19['content'].split('\n')
    print("Start:", '\n'.join(lines19[:5]))
    print("...")
    print("End:", '\n'.join(lines19[-10:]))
    
    # Save script 19 to file
    with open('script19.js', 'w', encoding='utf-8') as f:
        f.write(s19['content'])
except Exception as e:
    print("Error getting script 19:", e)

