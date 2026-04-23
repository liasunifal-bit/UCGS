import sys
import codecs

filepath = r"C:\Users\maria\Downloads\sistema_UGA_v23 (1).html"
try:
    with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if 'Nutri' in line or 'sidebar-bg' in line or '</body>' in line or '</style>' in line:
            print(f"{i+1}: {line.strip()}")
            
except Exception as e:
    print(f"Error: {e}")
