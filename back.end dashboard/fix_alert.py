import sys

file_path = 'site nevo.HTML'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "            } catch (err) {\n                console.error('Erro de login:', err);\n                alertM.textContent = 'Erro Supabase: ' + err.message;\n                showAlert('INVALID');"

    replacement = "            } catch (err) {\n                console.error('Erro de login:', err);\n                showAlert('INVALID');\n                alertM.textContent = 'Erro Supabase: ' + err.message;"

    if target in content:
        content = content.replace(target, replacement)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[OK] Swap completed.')
    else:
        print('[ERROR] Target not found.')
except Exception as e:
    print('Error:', e)
