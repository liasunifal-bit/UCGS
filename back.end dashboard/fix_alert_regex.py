import sys
import re

file_path = 'site nevo.HTML'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to find:
    # console.error('Erro de login:', err);
    # alertM.textContent = 'Erro Supabase: ' + err.message;
    # showAlert('INVALID');
    #
    # And swap the last two lines.

    pattern = re.compile(
        r"(console\.error\('Erro de login:', err\);\s*)"
        r"(alertM\.textContent = 'Erro Supabase: ' \+ err\.message;\s*)"
        r"(showAlert\('INVALID'\);)"
    )

    if pattern.search(content):
        content = pattern.sub(r"\1\3\n                \2", content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[OK] Swap completed via regex.')
    else:
        print('[ERROR] Target not found with regex.')
except Exception as e:
    print('Error:', e)
