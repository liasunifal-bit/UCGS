import os

def fix_mojibake(content):
    # Mapping of common mojibake patterns (from double or triple encoding)
    # These are sequences found in Brazilian Portuguese clinical systems
    replacements = [
        # Level 3 (Triple encoding)
        ('ÃƒÆ’Ã‚Â£', 'ã'),
        ('ÃƒÆ’Ã‚Â§', 'ç'),
        ('ÃƒÆ’Ã‚Â¡', 'á'),
        ('ÃƒÆ’Ã‚Â©', 'é'),
        ('ÃƒÆ’Ã‚Â³', 'ó'),
        ('ÃƒÆ’Ã‚Âº', 'ú'),
        ('ÃƒÆ’Ã‚Âª', 'ê'),
        ('ÃƒÆ’Ã‚Â´', 'ô'),
        ('ÃƒÆ’Ã‚Âµ', 'õ'),
        ('ÃƒÆ’Ã‚Â', 'í'),
        ('ÃƒÆ’Ã¢â‚¬Â¡', 'Ç'),
        ('ÃƒÆ’Ã†â€™', 'Ã'),
        
        # Level 2 (Double encoding)
        ('ÃƒÂ£', 'ã'),
        ('ÃƒÂ§', 'ç'),
        ('ÃƒÂ¡', 'á'),
        ('ÃƒÂ©', 'é'),
        ('ÃƒÂ³', 'ó'),
        ('ÃƒÂº', 'ú'),
        ('ÃƒÂª', 'ê'),
        ('ÃƒÂ´', 'ô'),
        ('ÃƒÂµ', 'õ'),
        ('ÃƒÂ', 'í'),
        ('Ãƒâ€¡', 'Ç'),
        ('Ãƒâ€¹', 'Ë'),
        ('Ãƒâ€š', 'Â'),
        ('Ãƒâ€ ', 'À'),
        ('ÃƒÂ ', 'à'),
        ('ÃƒÂ¢', 'â'),
        ('ÃƒÂª', 'ê'),
        ('ÃƒÂ®', 'î'),
        ('ÃƒÂ´', 'ô'),
        ('ÃƒÂ»', 'û'),
        ('Ãƒâ€°', 'É'),
        
        # Specific double-encoded patterns from the audit
        ('\xc3\x83\xe2\x80\xa1', 'Ç'), # Ã‡ -> Ç
        ('\xc3\x83\xc6\x92', 'Ã'),     # Ãƒ -> Ã
        
        # Level 1 (Single encoding error)
        ('Ã¡', 'á'), ('Ã©', 'é'), ('Ã\xad', 'í'), ('Ã³', 'ó'), ('Ãº', 'ú'),
        ('Ã¢', 'â'), ('Ãª', 'ê'), ('Ã´', 'ô'), ('Ã»', 'û'),
        ('Ã£', 'ã'), ('Ãµ', 'õ'),
        ('Ã§', 'ç'),
        ('Ã€', 'À'), ('Ã\x81', 'Á'), ('Ã\x89', 'É'), ('Ã\x8d', 'Í'), ('Ã\x93', 'Ó'), ('Ã\x9a', 'Ú'),
        ('Ã\x87', 'Ç'),
        ('Ã\x82', 'Â'), ('Ã\x8a', 'Ê'), ('Ã\x94', 'Ô'),
        ('Ã\x83', 'Ã'),
        
        # Special symbols and dashes
        ('Ã¢â‚¬â€', '—'),
        ('Ã¢â‚¬â€œ', '–'),
        ('Ã¢â‚¬â„¢', '’'),
        ('Ã¢â‚¬Å“', '“'),
        ('Ã¢â‚¬Â', '”'),
        ('Ã¢â‚¬Â¦', '…'),
        ('Ã‚Â', ''), # Non-breaking space often shows up as this
        
        # Specific clinical terms that often get truncated or missed
        ('MANUTENO', 'MANUTENÇÃO'),
        ('notificao', 'notificação'),
        ('notificaÃ§Ã£o', 'notificação'),
        ('revisÃ£o', 'revisão'),
        ('Vacinao', 'Vacinação'),
        ('VacinAÃ§Ã£o', 'Vacinação'),
        ('Carto', 'Cartão'),
        ('CartÃ£o', 'Cartão'),
        ('Ateno', 'Atenção'),
        ('Descrio', 'Descrição'),
        ('Informaes', 'Informações'),
        ('Configuraes', 'Configurações'),
        ('AÃ§Ã£o', 'Ação'),
        ('AÃ§Ãµes', 'Ações'),
        ('VisÃ£o', 'Visão')
    ]

    for old, new in replacements:
        if isinstance(old, bytes):
            # If it's bytes, we need to find it in the byte array or a decoded latin-1 string
            # For simplicity, we'll assume the caller passes a string decoded as latin-1
            old_str = old.decode('latin-1')
            content = content.replace(old_str, new)
        else:
            content = content.replace(old, new)
            
    return content

def main():
    backup_path = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo_backup_encoding.HTML'
    output_path = r'c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML'

    print(f"Lendo backup: {backup_path}")
    with open(backup_path, 'rb') as f:
        data = f.read()

    # Decode as latin-1 to handle ALL bytes as characters
    content = data.decode('latin-1')

    print("Corrigindo mojibake...")
    content = fix_mojibake(content)

    print(f"Salvando resultado: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Limpeza concluída com sucesso!")

if __name__ == "__main__":
    main()
