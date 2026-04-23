#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix definitivo:
1. Remove todos os blocos Lucide injetados anteriormente (inclusive o que ficou dentro de w.document.write)
2. Re-injeta Lucide no lugar CORRETO (último </script> antes do verdadeiro </body>)
3. Usa aspas simples nos atributos data-lucide para não quebrar strings JS com aspas duplas
4. Corrige o erro 'submit is not defined' no patch de login
"""
import re

DEST = "site nevo.HTML"

with open(DEST, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Remover TODOS os blocos Lucide injetados ────────────────────
# Remove o script tag com lucide.min.js onde quer que apareça
content = re.sub(
    r'\s*<!-- Lucide Icons[^>]*?-->\s*<script src="lucide\.min\.js"></script>',
    '', content
)
content = re.sub(
    r'\s*<script src="lucide\.min\.js"></script>',
    '', content
)
# Remove bloco de init Lucide
content = re.sub(
    r'\s*<script>\s*(?://[^\n]*\n)*\s*(?:if \(typeof lucide|window\._lucideRefresh|var _lcObserver).*?</script>',
    '', content, flags=re.DOTALL
)
print("[1] Blocos Lucide anteriores removidos")

# ── 2. Corrigir atributos data-lucide para usar ASPAS SIMPLES ─────
# Isso evita quebrar strings JS com aspas duplas
content = content.replace(
    'data-lucide="', "data-lucide='"
).replace(
    '"></i>', "'></i>"
)
print("[2] Atributos data-lucide convertidos para aspas simples")

# ── 3. Encontrar o verdadeiro </body> final ────────────────────────
# O verdadeiro </body> deve ser o ÚLTIMO no arquivo
last_body_idx = content.rfind("</body>")
if last_body_idx < 0:
    print("[ERRO] </body> não encontrado!")
    exit(1)
print(f"[3] Verdadeiro </body> encontrado na posição {last_body_idx:,}")

# ── 4. Injetar Lucide antes do </body> final ───────────────────────
LUCIDE_BLOCK = """
    <!-- Lucide Icons: carregado no final do body -->
    <script src="lucide.min.js"></script>
    <script>
        (function() {
            function initLucide() {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                } else {
                    // Retry em 300ms se ainda não carregou
                    setTimeout(initLucide, 300);
                }
            }
            initLucide();
            window._lucideRefresh = function() {
                if (typeof lucide !== 'undefined') lucide.createIcons();
            };
            // Re-inicializa ao navegar entre seções
            document.addEventListener('click', function(e) {
                var t = e.target.closest('[data-section]');
                if (t) setTimeout(function() {
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                }, 150);
            });
        })();
    </script>
"""

content = content[:last_body_idx] + LUCIDE_BLOCK + content[last_body_idx:]
print("[4] Lucide injetado antes do </body> final")

# ── 5. Corrigir erro 'submit is not defined' no patch de login ─────
# O problema é que 'submit' é referenciado antes de ser declarado no patch
# Precisa ser declarado como querySelector dentro do try block
old_login_ref = "submit.querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';"
new_login_ref = "form.querySelector('[type=\"submit\"]').querySelector('.ucgs-login-submit-label').textContent = 'Acesso autorizado';"

if old_login_ref in content:
    content = content.replace(old_login_ref, new_login_ref)
    print("[5] Referência 'submit' corrigida para querySelector")
else:
    # Alternativa: fix via regex
    content = re.sub(
        r'\bsubmit\.querySelector\(',
        "form.querySelector('[type=\"submit\"]').querySelector(",
        content
    )
    print("[5] Referência 'submit' corrigida via regex")

# ── 6. Adicionar logo placeholder se não existir ──────────────────
# (logo ucgs.png 404 é cosmético, mas podemos criar um placeholder inline)
# Substituir src da logo por data URI de placeholder SVG
LOGO_PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'%3E%3Ccircle cx='24' cy='24' r='22' fill='%230EA5E9'/%3E%3Ctext x='24' y='30' text-anchor='middle' fill='white' font-size='14' font-weight='bold' font-family='Inter,sans-serif'%3EUCGS%3C/text%3E%3C/svg%3E"

# Só substituir se o arquivo não existe
import os
if not os.path.exists("logo ucgs.png") and not os.path.exists("logo%20ucgs.png"):
    content = content.replace('src="logo%20ucgs.png"', f'src="{LOGO_PLACEHOLDER}"')
    content = content.replace("src='logo%20ucgs.png'", f"src='{LOGO_PLACEHOLDER}'")
    content = content.replace('src="logo ucgs.png"', f'src="{LOGO_PLACEHOLDER}"')
    content = content.replace("src='logo ucgs.png'", f"src='{LOGO_PLACEHOLDER}'")
    print("[6] Logo placeholder injetado (SVG inline)")
else:
    print("[6] Logo arquivo existe, sem alteração")

# ── 7. Salvar ──────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n[OK] Salvo ({len(content):,} chars)")
print("Pressione Ctrl+F5 no navegador!")
