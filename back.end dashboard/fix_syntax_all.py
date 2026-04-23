import re
import subprocess
import os

file_path = 'site nevo.HTML'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the quotes inside strings
# Before: '<i data-lucide='icon-name'></i>'
# After: '<i data-lucide="icon-name"></i>'
new_content = re.sub(r"<i data-lucide='([^']+)'>", r'<i data-lucide="\1">', content)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('[OK] Fixed data-lucide quotes.')
else:
    print('[INFO] No changes needed.')

# Validate scripts again
scripts = re.findall(r'<script[^>]*>(.*?)</script>', new_content, re.DOTALL)
errors = 0
for i, script in enumerate(scripts):
    if script.strip():
        temp_file = f'temp_script_{i}.js'
        with open(temp_file, 'w', encoding='utf-8') as tf:
            tf.write(script)
        
        result = subprocess.run(['node', '-c', temp_file], capture_output=True, text=True)
        if result.returncode != 0:
            print(f'\\n--- SyntaxError in script {i} ---')
            print(result.stderr)
            errors += 1
        
        try:
            os.remove(temp_file)
        except:
            pass

if errors == 0:
    print('[OK] ALL JS SCRIPTS SYNTAX VALIDATED SUCCESSFULLY.')
