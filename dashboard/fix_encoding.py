
import os

path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'

def fix_content():
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Fix Supabase init (remove onload)
    new_content = content.replace('onload="initSupabase()"', '')

    # 2. Fix Mojibake
    replacements = {
        'ðŸ’¡': '💡',
        'MANUTENÃ‡ÃƒO': 'MANUTENÇÃO',
        'AÃ‡ÃƒO': 'AÇÃO',
        'INFORMAÃ‡Ã•ES': 'INFORMAÇÕES',
        'SITUAÃ‡ÃƒO': 'SITUAÇÃO',
        'NOTIFICAÃ‡Ã•ES': 'NOTIFICAÇÕES',
        'CONFIGURAÃ‡Ã•ES': 'CONFIGURAÇÕES',
        'DESCRIÃ‡ÃƒO': 'DESCRIÇÃO',
        'PREVENÃ‡ÃƒO': 'PREVENÇÃO',
        'ATUALIZAÃ‡ÃƒO': 'ATUALIZAÇÃO',
        'OBSERVAÃ‡ÃƒO': 'OBSERVAÇÃO',
        'MÃ‰DICO': 'MÉDICO',
        'PROFISSIONÃRIO': 'PROFISSIONÁRIO',
        'SAÃšDE': 'SAÚDE',
        'ÃšLTIMOS': 'ÚLTIMOS',
        'PRONTUÃRIO': 'PRONTUÁRIO',
        'HISTÃ“RICO': 'HISTÓRICO',
        'PACIENTE': 'PACIENTE',
        'MÃŠS': 'MÊS',
        'ÃREA': 'ÁREA',
        'PÃGINA': 'PÁGINA',
        'ÃCONE': 'ÍCONE'
    }

    for old, new in replacements.items():
        if old in new_content:
            print(f"Fixing {old} -> {new}")
            new_content = new_content.replace(old, new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fix complete. File size:", len(new_content))

if __name__ == "__main__":
    fix_content()
