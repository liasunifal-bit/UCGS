import sys

file_path = 'site nevo.HTML'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find boundaries of the duplicate authenticate logic
    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if 'const authenticate = () => {' in line:
            start_idx = i
        elif start_idx != -1 and end_idx == -1 and 'authenticate();' in line:
            end_idx = i + 2 # Skip the closing bracket of the listener

    if start_idx != -1 and end_idx != -1:
        del lines[start_idx:end_idx]
        print(f"Removed duplicate authenticate logic from {start_idx} to {end_idx}")
    
    # Add real error message to catch block
    for i, line in enumerate(lines):
        if "console.error('Erro de login:', err);" in line:
            lines.insert(i+1, "                alertM.textContent = 'Erro Supabase: ' + err.message;\n")
            print("Enhanced error message in catch block.")
            break

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("[OK] Modifications completed.")
except Exception as e:
    print("Error:", e)
