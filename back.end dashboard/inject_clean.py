import re

file_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/site nevo.HTML'
js_path = 'c:/Users/maria/Downloads/antigravity lias/back.end dashboard/supabase-client.js'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Ache onde está </body> e injeta antes
idx = html.rfind('</body>')

if idx != -1:
    injected = f'''\n\n<!-- ============================================================
INTEGRACAO SUPABASE - CONEXAO COM O BACKEND
============================================================ -->
<script>
{js_content}

window.addEventListener('DOMContentLoaded', async () => {{
    console.log('🔄 Iniciando conexao com o banco de dados Supabase...');
    try {{
        const perfis = await SupabaseClient.from('profiles').get();
        console.log('✅ Conexao bem-sucedida! Dados carregados do banco:', perfis);
    }} catch (error) {{
        console.error('❌ Erro na conexao com o Supabase:', error.message);
    }}
}});
</script>\n'''
    
    new_html = html[:idx] + injected + html[idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Sucesso!")
else:
    print("nao achou body")
