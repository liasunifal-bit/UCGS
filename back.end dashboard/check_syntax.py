import re
import subprocess
import os

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extrair conteudos de tags <script> que contem conteudo e nao sao links
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)

print(f"Total de blocos de script encontrados: {len(scripts)}")

error_count = 0
for i, script_content in enumerate(scripts):
    if not script_content.strip():
        continue
    
    temp_file = f"temp_script_{i}.js"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    try:
        # Run node -c to check syntax
        result = subprocess.run(['node', '-c', temp_file], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"--- Erro de sintaxe no Script {i} ---")
            print(result.stderr)
            error_count += 1
            
            # Print as primeiras e ultimas linhas para identificar
            lines = script_content.strip().split('\n')
            if len(lines) > 5:
                print("Inicio do script:")
                print('\n'.join(lines[:3]))
                print("...")
                print('\n'.join(lines[-3:]))
            else:
                print("Script:", script_content)
            print("---------------------------------")
    except Exception as e:
        print("Erro rodando node:", e)
    
    try:
        os.remove(temp_file)
    except:
        pass

if error_count == 0:
    print("Nenhum erro de sintaxe detectado nos scripts!")
else:
    print(f"Encontrados {error_count} blocos com erro de sintaxe.")
