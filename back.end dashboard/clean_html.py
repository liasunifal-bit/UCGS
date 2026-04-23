import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern para encontrar e remover todas as injecoes do SupabaseClient (versao string injetada com document.write e a do footer)
# As injecoes comecam com: <!-- ======... INTEGRA... SUPABASE ou algo parecido
# Ou começam com "const SupabaseClient = (function () {"

# O erro de sintaxe na linha 18237 é porque eu injetei quebrando uma string JavaScript.
# Vamos remover TUDO entre '    <!-- \n============================================================\n         INTEGRAÇÃO SUPABASE' e '</script>'
# Mas note que os caracteres de acento podem estar zuados.

pattern1 = re.compile(r'\s*<!-- [=]+\s*INTEGRA.*?CONEX.*?BACKEND\s*[=]+ -->\s*<script>\s*const SupabaseClient =.*?</script>', re.DOTALL | re.IGNORECASE)
content_cleaned = pattern1.sub('', content)

# Remove any document.write('<!-- ... SUPABASE ... </script>
pattern2 = re.compile(r"w\.document\.write\('\s*<!-- [=]+.*?</script>'\);", re.DOTALL | re.IGNORECASE)
content_cleaned = pattern2.sub('', content_cleaned)

# Achar outras declaracoes de const SupabaseClient e remover o bloco de script em volta
pattern3 = re.compile(r'\s*/\*\*\s*\*\s*UCGS.*?Supabase.*?const SupabaseClient =.*?</script>', re.DOTALL | re.IGNORECASE)
content_cleaned = pattern3.sub('', content_cleaned)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_cleaned)
print("Limpeza concluida.")
