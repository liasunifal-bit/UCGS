import os

def fix_encoding(file_path):
    replacements = {
        'Ã‡': 'Ç',
        'Ãƒ': 'Ã',
        'Ã‰': 'É',
        'Ãª': 'ê',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã¡': 'á',
        'Ã§': 'ç',
        'Ãµ': 'õ',
        'Ã©': 'é',
        'Ã\xad': 'í', 
        'â€”': '—',
        'â€“': '–',
        'PROTOCOLOS DE ACIDENTES ': 'PROTOCOLOS DE ACIDENTES —',
        'MANUTENO': 'MANUTENÇÃO',
        'Botes': 'Botões',
        'SEO': 'SEÇÃO',
        'NUTRIO': 'NUTRIÇÃO',
        'Validao': 'Validação',
        'Padro': 'Padrão',
        'idntico': 'idêntico',
        'Informaes': 'Informações',
        'Configuraes': 'Configurações',
        'Ateno': 'Atenção',
        'Descrio': 'Descrição',
        'AÃ§Ã£o': 'Ação',
        'AÃ§Ãµes': 'Ações'
    }

    print(f"Lendo {file_path}...")
    with open(file_path, 'rb') as f:
        content_bytes = f.read()

    content = content_bytes.decode('latin-1')
    
    print("Aplicando substituições...")
    for old, new in replacements.items():
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            print(f"Substituído '{old}' por '{new}' ({count} ocorrências)")

    print(f"Salvando {file_path} como UTF-8...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Arquivo {file_path} corrigido com sucesso.")

if __name__ == "__main__":
    target_file = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML'
    fix_encoding(target_file)
