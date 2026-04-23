import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# find index of 'form.addEventListener(\'submit\''
idx = content.find("form.addEventListener('submit'")
if idx != -1:
    end_idx = content.find("});", idx)
    print("Encontrado evento submit:")
    print(content[idx:end_idx+3])
else:
    print("Nao achou o submit")
