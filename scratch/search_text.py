import sys

file_path = r'c:\Users\maria\Downloads\antigravity lias\dashboard\index.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except UnicodeDecodeError:
    with open(file_path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

search_terms = ['REVER', 'VACINA', 'PROTOCOLO', 'DETENTO']

for i, line in enumerate(lines):
    for term in search_terms:
        if term in line:
            print(f"Line {i+1}: {line.strip()}")
