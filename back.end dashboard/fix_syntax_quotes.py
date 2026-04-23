import sys

file_path = 'site nevo.HTML'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    target_1 = "console.log('<i data-lucide='rotate-cw'></i> Iniciando conexao com o banco de dados Supabase...');"
    target_2 = "console.log('<i data-lucide='circle-check'></i> Conexao bem-sucedida! Dados carregados do banco:', perfis);"

    replacement_1 = "console.log(`<i data-lucide='rotate-cw'></i> Iniciando conexao com o banco de dados Supabase...`);"
    replacement_2 = "console.log(`<i data-lucide='circle-check'></i> Conexao bem-sucedida! Dados carregados do banco:`, perfis);"

    if target_1 in content and target_2 in content:
        content = content.replace(target_1, replacement_1)
        content = content.replace(target_2, replacement_2)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[OK] SyntaxError fixed.')
    else:
        print('[ERROR] Targets not found.')
except Exception as e:
    print('Error:', e)
