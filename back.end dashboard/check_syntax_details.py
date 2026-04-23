import re
import subprocess
import os
import sys

# Forcar utf-8 no stdout
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

scripts = []
for m in re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE):
    code = m.group(1).strip()
    if code:
        scripts.append({
            'start_line': content.count('\n', 0, m.start()) + 1,
            'end_line': content.count('\n', 0, m.end()) + 1,
            'content': code
        })

print(f"Total de blocos de script encontrados: {len(scripts)}")

error_count = 0
for i, s in enumerate(scripts):
    temp_file = f"temp_script_{i}.js"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(s['content'])
    
    result = subprocess.run(['node', '-c', temp_file], capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"\n--- Erro de sintaxe no Script {i} (Linhas {s['start_line']} ate {s['end_line']}) ---")
        print(result.stderr)
        error_count += 1
    
    try:
        os.remove(temp_file)
    except:
        pass

print(f"\nConcluido! Encontrados {error_count} erros.")
