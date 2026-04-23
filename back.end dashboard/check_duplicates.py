import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Contar quantas vezes aparece const SupabaseClient = (function () {
count = content.count('const SupabaseClient = (function () {')
print(f"Total de declaracoes: {count}")

# Vamos manter apenas a PRIMEIRA declaracao de SupabaseClient
# mas esperar, onde o SupabaseClient foi injetado? Eu injetei no final do body.
# Porem as outras injecoes parecem ter <script>...</script>
