import sys

file_path = 'site nevo.HTML'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is exactly:
    #             w.document.write('
    # </body></html>');
    
    target = "            w.document.write('\n</body></html>');"
    replacement = "            w.document.write('</body></html>');"
    
    if target in content:
        content = content.replace(target, replacement)
        print("Replaced exact newline syntax error.")
    else:
        print("Target not found exactly, trying regex...")
        import re
        content, n = re.subn(r"w\.document\.write\('\s*</body></html>'\);", r"w.document.write('</body></html>');", content)
        print(f"Replaced {n} occurrences via regex.")
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print('[OK] SyntaxError fixed.')
except Exception as e:
    print("Error:", e)
